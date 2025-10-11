"""WhatsApp Cloud API client for sending messages."""
import httpx
from typing import Optional, Dict, Any
from src.config import settings
from src.logger import get_logger

logger = get_logger(__name__)


class WhatsAppClient:
    """Client for interacting with WhatsApp Cloud API."""
    
    def __init__(self):
        self.base_url = settings.whatsapp_api_base_url
        self.phone_number_id = settings.whatsapp_phone_number_id
        self.access_token = settings.whatsapp_access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    async def send_text_message(self, to: str, message: str) -> Dict[str, Any]:
        """
        Send a text message via WhatsApp Cloud API.
        
        Args:
            to: Recipient phone number (e.g., "+5491112345678")
            message: Text message to send
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to.replace("+", ""),  # Remove + from phone number
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        
        logger.info(f"Sending text message to {to}")
        logger.debug(f"Payload: {payload}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self.headers,
                    timeout=30.0
                )
                
                response_data = response.json()
                
                if response.status_code == 200:
                    logger.info(f"Message sent successfully to {to}")
                    logger.debug(f"Response: {response_data}")
                    return {
                        "success": True,
                        "data": response_data
                    }
                else:
                    logger.error(f"Failed to send message: {response.status_code} - {response_data}")
                    return {
                        "success": False,
                        "error": response_data,
                        "status_code": response.status_code
                    }
                    
        except httpx.TimeoutException:
            logger.error(f"Timeout while sending message to {to}")
            return {
                "success": False,
                "error": "Request timeout"
            }
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_image_message(self, to: str, image_url: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """
        Send an image message via WhatsApp Cloud API.
        
        Args:
            to: Recipient phone number
            image_url: URL of the image to send
            caption: Optional caption for the image
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to.replace("+", ""),
            "type": "image",
            "image": {
                "link": image_url
            }
        }
        
        if caption:
            payload["image"]["caption"] = caption
        
        logger.info(f"Sending image message to {to}")
        logger.debug(f"Payload: {payload}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self.headers,
                    timeout=30.0
                )
                
                response_data = response.json()
                
                if response.status_code == 200:
                    logger.info(f"Image sent successfully to {to}")
                    return {
                        "success": True,
                        "data": response_data
                    }
                else:
                    logger.error(f"Failed to send image: {response.status_code} - {response_data}")
                    return {
                        "success": False,
                        "error": response_data,
                        "status_code": response.status_code
                    }
                    
        except Exception as e:
            logger.error(f"Error sending image: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

