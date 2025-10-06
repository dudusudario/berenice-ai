"""
Dashboard API endpoints for monitoring conversations.
"""
import logging
from typing import List, Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from datetime import datetime
from services.websocket_service import ws_manager
from api.webhooks import conversation_states
from services.graphiti_service import graphiti_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time dashboard updates.

    Client connects here to receive live updates of all conversations.
    """
    await ws_manager.connect(websocket)

    try:
        while True:
            # Keep connection alive and receive any client messages
            data = await websocket.receive_text()

            # Handle client commands if needed
            if data == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        logger.info("Dashboard disconnected")


@router.get("/conversations")
async def get_conversations():
    """
    Get all active conversations.

    Returns:
        List of active conversation states
    """
    try:
        conversations = []

        for phone, state in conversation_states.items():
            conversations.append({
                "phone": phone,
                "patient_name": state.get("patient_name", "Unknown"),
                "started_at": state.get("started_at").isoformat() if state.get("started_at") else None,
                "messages_count": state.get("messages_count", 0),
                "last_activity": state.get("started_at").isoformat() if state.get("started_at") else None,
            })

        return {
            "success": True,
            "total": len(conversations),
            "conversations": conversations
        }

    except Exception as e:
        logger.error(f"Error getting conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/{phone}")
async def get_conversation_history(phone: str, limit: int = 50):
    """
    Get conversation history for a specific patient.

    Args:
        phone: Patient phone number
        limit: Maximum number of messages to retrieve

    Returns:
        Conversation history from Graphiti
    """
    try:
        # Get history from Graphiti
        history = await graphiti_service.get_patient_context(phone, limit=limit)

        return {
            "success": True,
            "phone": phone,
            "messages": history
        }

    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_stats():
    """
    Get system statistics.

    Returns:
        System stats including active conversations, total messages, etc.
    """
    try:
        total_conversations = len(conversation_states)
        total_messages = sum(
            state.get("messages_count", 0) for state in conversation_states.values()
        )

        active_connections = len(ws_manager.active_connections)

        stats = {
            "active_conversations": total_conversations,
            "total_messages": total_messages,
            "dashboard_connections": active_connections,
            "graphiti_status": "connected" if graphiti_service.graphiti else "disconnected",
            "timestamp": datetime.now().isoformat()
        }

        return {
            "success": True,
            "stats": stats
        }

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send-message")
async def send_manual_message(phone: str, message: str):
    """
    Send a manual message to a patient (human intervention).

    Args:
        phone: Patient phone number
        message: Message to send

    Returns:
        Success response
    """
    try:
        from services.zapi_service import zapi_service

        # Send message via Z-API
        result = await zapi_service.send_text(phone, message)

        # Broadcast to dashboard
        await ws_manager.broadcast_outgoing_message(
            phone=phone,
            patient_name=conversation_states.get(phone, {}).get("patient_name", "Unknown"),
            message_text=message,
        )

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        logger.error(f"Error sending manual message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversation/{phone}")
async def clear_conversation(phone: str):
    """
    Clear a conversation from active states.

    Args:
        phone: Patient phone number

    Returns:
        Success response
    """
    try:
        if phone in conversation_states:
            del conversation_states[phone]

            await ws_manager.broadcast({
                "type": "conversation_cleared",
                "phone": phone,
                "timestamp": datetime.now().isoformat()
            })

            return {
                "success": True,
                "message": f"Conversation cleared for {phone}"
            }
        else:
            raise HTTPException(status_code=404, detail="Conversation not found")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
