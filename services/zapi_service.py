"""
Z-API Service for WhatsApp integration.
"""
import httpx
import logging
from typing import Dict, Any, Optional, List
from config.settings import settings

logger = logging.getLogger(__name__)


class ZAPIService:
    """Client for Z-API WhatsApp integration."""

    def __init__(
        self,
        instance_id: Optional[str] = None,
        token: Optional[str] = None,
        client_token: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.instance_id = instance_id or settings.zapi_instance_id
        self.token = token or settings.zapi_token
        self.client_token = client_token or settings.zapi_client_token
        self.base_url = base_url or settings.zapi_base_url

        if not all([self.instance_id, self.token, self.client_token]):
            raise ValueError(
                "Z-API credentials not configured. Please check your .env file."
            )

        self.base_url = f"{self.base_url}/instances/{self.instance_id}/token/{self.token}"
        self.headers = {"Client-Token": self.client_token, "Content-Type": "application/json"}

    async def send_text(
        self, phone: str, message: str
    ) -> Dict[str, Any]:
        """
        Send a text message to a WhatsApp number.

        Args:
            phone: Phone number with country code (e.g., 5511999999999)
            message: Text message to send

        Returns:
            Response from Z-API
        """
        url = f"{self.base_url}/send-text"
        payload = {"phone": phone, "message": message}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=payload, headers=self.headers, timeout=30.0
                )
                response.raise_for_status()
                logger.info(f"Message sent to {phone}")
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to send message to {phone}: {e}")
            raise

    async def send_image(
        self, phone: str, image_url: str, caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an image to a WhatsApp number.

        Args:
            phone: Phone number with country code
            image_url: URL of the image to send
            caption: Optional caption for the image

        Returns:
            Response from Z-API
        """
        url = f"{self.base_url}/send-image"
        payload = {"phone": phone, "image": image_url}

        if caption:
            payload["caption"] = caption

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=payload, headers=self.headers, timeout=30.0
                )
                response.raise_for_status()
                logger.info(f"Image sent to {phone}")
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to send image to {phone}: {e}")
            raise

    async def send_file(
        self, phone: str, file_url: str, filename: str, caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a file (PDF, document) to a WhatsApp number.

        Args:
            phone: Phone number with country code
            file_url: URL of the file to send
            filename: Name of the file
            caption: Optional caption for the file

        Returns:
            Response from Z-API
        """
        url = f"{self.base_url}/send-document"
        payload = {"phone": phone, "document": file_url, "fileName": filename}

        if caption:
            payload["caption"] = caption

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=payload, headers=self.headers, timeout=30.0
                )
                response.raise_for_status()
                logger.info(f"File sent to {phone}")
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to send file to {phone}: {e}")
            raise

    async def send_button_list(
        self,
        phone: str,
        title: str,
        description: str,
        buttons: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Send a message with button list.

        Args:
            phone: Phone number with country code
            title: Title of the message
            description: Description text
            buttons: List of buttons [{"id": "1", "label": "Option 1"}, ...]

        Returns:
            Response from Z-API
        """
        url = f"{self.base_url}/send-button-list"
        payload = {
            "phone": phone,
            "title": title,
            "description": description,
            "buttons": buttons,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=payload, headers=self.headers, timeout=30.0
                )
                response.raise_for_status()
                logger.info(f"Button list sent to {phone}")
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to send button list to {phone}: {e}")
            raise

    async def mark_as_read(self, phone: str, message_id: str) -> Dict[str, Any]:
        """
        Mark a message as read.

        Args:
            phone: Phone number with country code
            message_id: ID of the message to mark as read

        Returns:
            Response from Z-API
        """
        url = f"{self.base_url}/read-message"
        payload = {"phone": phone, "messageId": message_id}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=payload, headers=self.headers, timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to mark message as read: {e}")
            raise

    async def typing_on(self, phone: str) -> Dict[str, Any]:
        """
        Show typing indicator (digitando...).

        Args:
            phone: Phone number with country code

        Returns:
            Response from Z-API
        """
        url = f"{self.base_url}/send-presence"
        payload = {"phone": phone, "status": "composing"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=payload, headers=self.headers, timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to set typing status: {e}")
            raise

    async def typing_off(self, phone: str) -> Dict[str, Any]:
        """
        Hide typing indicator.

        Args:
            phone: Phone number with country code

        Returns:
            Response from Z-API
        """
        url = f"{self.base_url}/send-presence"
        payload = {"phone": phone, "status": "available"}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, json=payload, headers=self.headers, timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to clear typing status: {e}")
            raise

    async def get_profile_pic(self, phone: str) -> Dict[str, Any]:
        """
        Get profile picture URL of a contact.

        Args:
            phone: Phone number with country code

        Returns:
            Response from Z-API with profile picture URL
        """
        url = f"{self.base_url}/profile-picture"
        params = {"phone": phone}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url, params=params, headers=self.headers, timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to get profile picture: {e}")
            raise


# Global instance
zapi_service = ZAPIService()
