"""
Graphiti Service for knowledge graph management.
"""
import json
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from config.settings import settings

logger = logging.getLogger(__name__)


class GraphitiService:
    """Service for managing patient knowledge graph."""

    def __init__(self):
        self.graphiti: Optional[Graphiti] = None

    async def initialize(self):
        """Initialize Graphiti connection and build indices."""
        try:
            self.graphiti = Graphiti(
                settings.neo4j_uri,
                settings.neo4j_user,
                settings.neo4j_password,
            )
            await self.graphiti.build_indices_and_constraints()
            logger.info("Graphiti initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Graphiti: {e}")
            raise

    async def close(self):
        """Close Graphiti connection."""
        if self.graphiti:
            await self.graphiti.close()
            logger.info("Graphiti connection closed")

    async def add_conversation_episode(
        self,
        phone: str,
        patient_name: Optional[str],
        message_text: str,
        message_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add a conversation episode to the knowledge graph.

        Args:
            phone: Patient phone number
            patient_name: Patient name (if known)
            message_text: The message content
            message_type: Type of message (text, image, audio, etc.)
            metadata: Additional metadata (sentiment, intent, etc.)
        """
        if not self.graphiti:
            raise RuntimeError("Graphiti not initialized")

        try:
            # Build episode content
            if metadata:
                episode_content = {
                    "phone": phone,
                    "patient_name": patient_name,
                    "message": message_text,
                    "message_type": message_type,
                    **metadata,
                }
                episode_type = EpisodeType.json
                episode_body = json.dumps(episode_content)
            else:
                episode_body = f"Patient {patient_name or phone}: {message_text}"
                episode_type = EpisodeType.text

            # Add episode to graph
            await self.graphiti.add_episode(
                name=f"Conversation_{phone}_{datetime.now(timezone.utc).isoformat()}",
                episode_body=episode_body,
                source=episode_type,
                source_description=f"WhatsApp conversation with {patient_name or phone}",
                reference_time=datetime.now(timezone.utc),
            )

            logger.info(f"Added conversation episode for {phone}")
        except Exception as e:
            logger.error(f"Failed to add conversation episode: {e}")
            raise

    async def search_patient_history(
        self, query: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search patient history in the knowledge graph.

        Args:
            query: Search query (e.g., patient name, phone, treatment type)
            limit: Maximum number of results

        Returns:
            List of relevant facts from the knowledge graph
        """
        if not self.graphiti:
            raise RuntimeError("Graphiti not initialized")

        try:
            results = await self.graphiti.search(query, limit=limit)

            formatted_results = []
            for result in results:
                formatted_result = {
                    "uuid": result.uuid,
                    "fact": result.fact,
                    "source_node_uuid": (
                        result.source_node_uuid
                        if hasattr(result, "source_node_uuid")
                        else None
                    ),
                }

                if hasattr(result, "valid_at") and result.valid_at:
                    formatted_result["valid_at"] = str(result.valid_at)
                if hasattr(result, "invalid_at") and result.invalid_at:
                    formatted_result["invalid_at"] = str(result.invalid_at)

                formatted_results.append(formatted_result)

            logger.info(f"Found {len(formatted_results)} results for query: {query}")
            return formatted_results
        except Exception as e:
            logger.error(f"Failed to search patient history: {e}")
            raise

    async def add_patient_event(
        self,
        phone: str,
        patient_name: str,
        event_type: str,
        event_data: Dict[str, Any],
    ) -> None:
        """
        Add a significant patient event to the knowledge graph.

        Args:
            phone: Patient phone number
            patient_name: Patient name
            event_type: Type of event (appointment_scheduled, lead_qualified, etc.)
            event_data: Event details
        """
        if not self.graphiti:
            raise RuntimeError("Graphiti not initialized")

        try:
            episode_content = {
                "phone": phone,
                "patient_name": patient_name,
                "event_type": event_type,
                **event_data,
            }

            await self.graphiti.add_episode(
                name=f"Event_{event_type}_{phone}_{datetime.now(timezone.utc).isoformat()}",
                episode_body=json.dumps(episode_content),
                source=EpisodeType.json,
                source_description=f"Patient event: {event_type}",
                reference_time=datetime.now(timezone.utc),
            )

            logger.info(f"Added event {event_type} for patient {patient_name}")
        except Exception as e:
            logger.error(f"Failed to add patient event: {e}")
            raise

    async def get_patient_context(
        self, phone: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get comprehensive context about a patient.

        Args:
            phone: Patient phone number
            limit: Maximum number of results

        Returns:
            List of relevant patient facts
        """
        return await self.search_patient_history(phone, limit=limit)


# Global instance
graphiti_service = GraphitiService()
