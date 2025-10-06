"""
WebSocket service for real-time message broadcasting to dashboard.
"""
import logging
import json
from typing import Set, Dict, Any
from fastapi import WebSocket
from datetime import datetime

logger = logging.getLogger(__name__)


class WebSocketManager:
    """Manages WebSocket connections for the dashboard."""

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"New dashboard connection. Total: {len(self.active_connections)}")

        # Send initial state
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "timestamp": datetime.now().isoformat(),
            "message": "Connected to Berenice AI Dashboard"
        })

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        self.active_connections.discard(websocket)
        logger.info(f"Dashboard disconnected. Remaining: {len(self.active_connections)}")

    async def broadcast(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected dashboards.

        Args:
            message: Message data to broadcast
        """
        if not self.active_connections:
            return

        disconnected = set()

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message to dashboard: {e}")
                disconnected.add(connection)

        # Remove failed connections
        for connection in disconnected:
            self.disconnect(connection)

    async def broadcast_incoming_message(
        self,
        phone: str,
        sender_name: str,
        message_text: str,
        message_id: str,
    ):
        """
        Broadcast an incoming message from patient.

        Args:
            phone: Patient phone number
            sender_name: Patient name
            message_text: Message content
            message_id: Message ID
        """
        await self.broadcast({
            "type": "incoming_message",
            "direction": "input",
            "phone": phone,
            "sender_name": sender_name,
            "message": message_text,
            "message_id": message_id,
            "timestamp": datetime.now().isoformat(),
        })

    async def broadcast_outgoing_message(
        self,
        phone: str,
        patient_name: str,
        message_text: str,
        message_id: str = None,
    ):
        """
        Broadcast an outgoing message to patient.

        Args:
            phone: Patient phone number
            patient_name: Patient name
            message_text: Message content
            message_id: Message ID (optional)
        """
        await self.broadcast({
            "type": "outgoing_message",
            "direction": "output",
            "phone": phone,
            "patient_name": patient_name,
            "message": message_text,
            "message_id": message_id,
            "timestamp": datetime.now().isoformat(),
        })

    async def broadcast_agent_thinking(self, phone: str, status: str):
        """
        Broadcast agent thinking/processing status.

        Args:
            phone: Patient phone number
            status: Status message
        """
        await self.broadcast({
            "type": "agent_status",
            "phone": phone,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        })

    async def broadcast_stats(self, stats: Dict[str, Any]):
        """
        Broadcast system statistics.

        Args:
            stats: Statistics data
        """
        await self.broadcast({
            "type": "stats",
            "data": stats,
            "timestamp": datetime.now().isoformat(),
        })


# Global WebSocket manager instance
ws_manager = WebSocketManager()
