"""
Pydantic models for WhatsApp messages.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class WebhookMessage(BaseModel):
    """Model for incoming webhook message from Z-API."""

    instanceId: Optional[str] = None
    messageId: str
    phone: str
    fromMe: bool
    momment: int  # Timestamp in milliseconds
    status: Optional[str] = None
    chatName: Optional[str] = None
    senderPhoto: Optional[str] = None
    senderName: Optional[str] = None
    participantPhone: Optional[str] = None
    photo: Optional[str] = None
    broadcast: bool = False
    type: str = "ReceivedCallback"
    text: Optional[Dict[str, Any]] = None
    image: Optional[Dict[str, Any]] = None
    audio: Optional[Dict[str, Any]] = None
    video: Optional[Dict[str, Any]] = None
    document: Optional[Dict[str, Any]] = None
    sticker: Optional[Dict[str, Any]] = None
    location: Optional[Dict[str, Any]] = None
    contact: Optional[Dict[str, Any]] = None
    isGroup: bool = False
    isNewsletter: bool = False
    waitingMessage: bool = False

    def get_message_text(self) -> Optional[str]:
        """Extract text content from message."""
        if self.text:
            return self.text.get("message", "")
        elif self.image:
            return self.image.get("caption", "[Image]")
        elif self.video:
            return self.video.get("caption", "[Video]")
        elif self.document:
            return f"[Document: {self.document.get('fileName', 'file')}]"
        elif self.audio:
            return "[Audio message]"
        elif self.sticker:
            return "[Sticker]"
        elif self.location:
            return f"[Location: {self.location.get('latitude')}, {self.location.get('longitude')}]"
        elif self.contact:
            return f"[Contact: {self.contact.get('displayName', 'Unknown')}]"
        return None

    def get_sender_name(self) -> str:
        """Get sender name or phone."""
        return self.senderName or self.chatName or self.phone


class OutgoingMessage(BaseModel):
    """Model for outgoing message to be sent via Z-API."""

    phone: str
    message: str
    delay: Optional[int] = Field(default=None, description="Delay in seconds before sending")


class ConversationState(BaseModel):
    """Model for tracking conversation state."""

    phone: str
    patient_name: Optional[str] = None
    last_message_time: datetime
    awaiting_response: bool = False
    context: Dict[str, Any] = Field(default_factory=dict)
    lead_score: int = 0
    qualified: bool = False
    appointment_scheduled: bool = False
