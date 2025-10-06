"""
Webhook endpoints for receiving Z-API messages.
"""
import logging
import asyncio
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks, Request
from models.message import WebhookMessage
from services.zapi_service import zapi_service
from services.graphiti_service import graphiti_service
from config.prompts import get_welcome_message
from config.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhooks"])


# Simple in-memory storage for conversation states
# In production, use Redis or a database
conversation_states = {}


@router.post("/message")
async def receive_message(
    message: WebhookMessage,
    background_tasks: BackgroundTasks,
    request: Request,
):
    """
    Webhook endpoint to receive messages from Z-API.

    Args:
        message: Incoming message from Z-API
        background_tasks: FastAPI background tasks
        request: FastAPI request object

    Returns:
        Success response
    """
    try:
        # Ignore messages sent by us
        if message.fromMe:
            logger.info(f"Ignoring message from self: {message.messageId}")
            return {"status": "ignored", "reason": "message_from_self"}

        # Ignore group messages for now
        if message.isGroup:
            logger.info(f"Ignoring group message: {message.messageId}")
            return {"status": "ignored", "reason": "group_message"}

        # Extract message details
        phone = message.phone
        sender_name = message.get_sender_name()
        message_text = message.get_message_text()

        if not message_text:
            logger.warning(f"No text content in message {message.messageId}")
            return {"status": "ignored", "reason": "no_text_content"}

        logger.info(f"Received message from {sender_name} ({phone}): {message_text[:50]}...")

        # Add message processing to background tasks
        background_tasks.add_task(
            process_message,
            phone=phone,
            sender_name=sender_name,
            message_text=message_text,
            message_id=message.messageId,
        )

        return {"status": "received", "messageId": message.messageId}

    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


async def process_message(
    phone: str,
    sender_name: str,
    message_text: str,
    message_id: str,
):
    """
    Process incoming message from patient.

    This function runs in the background to avoid blocking the webhook response.

    Args:
        phone: Patient phone number
        sender_name: Patient name
        message_text: Message content
        message_id: Message ID
    """
    try:
        # Show typing indicator
        await zapi_service.typing_on(phone)

        # Add small delay to simulate human typing
        await asyncio.sleep(1)

        # Store conversation in Graphiti
        await graphiti_service.add_conversation_episode(
            phone=phone,
            patient_name=sender_name,
            message_text=message_text,
            metadata={
                "message_id": message_id,
                "timestamp": datetime.now().isoformat(),
            },
        )

        # Check if this is a new conversation
        is_new_conversation = phone not in conversation_states

        if is_new_conversation:
            # Send welcome message
            hour = datetime.now().hour
            welcome_msg = get_welcome_message(hour, settings.clinic_name)
            await zapi_service.send_text(phone, welcome_msg)

            # Initialize conversation state
            conversation_states[phone] = {
                "started_at": datetime.now(),
                "patient_name": sender_name,
                "messages_count": 1,
            }
        else:
            conversation_states[phone]["messages_count"] += 1

        # Process message with SDR agent
        from agent.sdr_agent import process_patient_message

        response = await process_patient_message(phone, sender_name, message_text)

        # Hide typing indicator
        await zapi_service.typing_off(phone)

        # Send response
        await zapi_service.send_text(phone, response)

        # Mark original message as read
        await zapi_service.mark_as_read(phone, message_id)

        logger.info(f"Successfully processed message from {phone}")

    except Exception as e:
        logger.error(f"Error in process_message: {e}", exc_info=True)
        # Try to inform the user about the error
        try:
            await zapi_service.send_text(
                phone,
                "Desculpe, ocorreu um erro ao processar sua mensagem. "
                "Por favor, tente novamente em instantes.",
            )
        except:
            pass


@router.post("/status")
async def receive_status(request: Request):
    """
    Webhook endpoint to receive message status updates from Z-API.

    Args:
        request: FastAPI request object

    Returns:
        Success response
    """
    try:
        data = await request.json()
        logger.info(f"Received status update: {data}")
        return {"status": "received"}
    except Exception as e:
        logger.error(f"Error processing status webhook: {e}")
        return {"status": "error", "message": str(e)}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "berenice-ai-webhook",
        "active_conversations": len(conversation_states),
    }
