"""Data models for WhatsApp integration."""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class NormalizedMessage(BaseModel):
    """Standardized message format for internal processing."""
    
    channel: Literal["whatsapp"] = "whatsapp"
    sender: str = Field(..., description="Phone number with country code, e.g., +54911...")
    message: str = Field(..., description="Message content")
    timestamp: str = Field(..., description="ISO format timestamp")
    message_id: Optional[str] = Field(None, description="Original message ID from WhatsApp")
    message_type: Optional[str] = Field("text", description="Type of message: text, image, etc.")


class SendMessageRequest(BaseModel):
    """Request model for sending WhatsApp messages."""
    
    to: str = Field(..., description="Recipient phone number with country code (e.g., +54911...)")
    message: str = Field(..., description="Message text to send")
    message_type: Literal["text", "image"] = Field("text", description="Type of message")
    media_url: Optional[str] = Field(None, description="URL of media (for image type)")


class SendMessageResponse(BaseModel):
    """Response model for send message endpoint."""
    
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    details: Optional[dict] = None


class WebhookVerification(BaseModel):
    """Model for webhook verification response."""
    
    challenge: str


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    service: str
    timestamp: str

