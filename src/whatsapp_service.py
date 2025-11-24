"""WhatsApp service with webhook listener and message sender."""
from fastapi import FastAPI, Request, HTTPException, Query, status
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import Dict, Any
from datetime import datetime
from src.models import (
    NormalizedMessage,
    SendMessageRequest,
    SendMessageResponse,
    HealthResponse
)
from src.config import settings
from src.logger import get_logger
from src.whatsapp_client import WhatsAppClient

logger = get_logger(__name__)

app = FastAPI(
    title="WhatsApp Integration Service",
    description="Service for receiving and sending WhatsApp messages via Meta Cloud API",
    version="1.0.0"
)

# Initialize WhatsApp client
whatsapp_client = WhatsAppClient()


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="WhatsApp Integration Service",
        timestamp=datetime.utcnow().isoformat()
    )


@app.get("/webhook/whatsapp")
async def verify_webhook(
    request: Request,
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """
    Webhook verification endpoint for Meta WhatsApp Cloud API.
    
    Meta will call this endpoint with verification parameters.
    We need to validate the verify_token and return the challenge.
    """
    logger.info("Webhook verification request received")
    logger.debug(f"Mode: {hub_mode}, Token: {hub_verify_token}")
    
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        logger.info("Webhook verified successfully")
        return PlainTextResponse(content=hub_challenge, status_code=200)
    else:
        logger.warning("Webhook verification failed - invalid token")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Verification token mismatch"
        )


@app.post("/webhook/whatsapp")
async def receive_webhook(request: Request):
    """
    Webhook endpoint to receive incoming WhatsApp messages and status updates.
    
    This endpoint receives events from Meta WhatsApp Cloud API and normalizes them
    to a standard format for internal processing.
    """
    try:
        body = await request.json()
        print("🔔 Webhook event received")
        logger.info("Webhook event received")
        logger.debug(f"Webhook payload: {body}")
        
        # Extract entry data
        if "entry" not in body:
            logger.warning("No entry field in webhook payload")
            return JSONResponse(content={"status": "no_entry"}, status_code=200)
        
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                
                # Process messages
                if "messages" in value:
                    for message in value["messages"]:
                        normalized = normalize_message(message, value)
                        print(f"📨 Normalized message: {normalized.dict()}")
                        logger.info(f"Normalized message: {normalized.dict()}")
                        
                        # Forward to Core API
                        await forward_to_core(normalized)
                        
                        # Auto-reply example (optional)
                        # await send_auto_reply(normalized.sender, normalized.message)
                
                # Process status updates
                if "statuses" in value:
                    for status_update in value["statuses"]:
                        logger.info(f"Status update: {status_update}")
                        # Handle delivery, read, sent statuses
        
        return JSONResponse(content={"status": "ok"}, status_code=200)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        # Always return 200 to Meta to avoid retries
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=200)


def normalize_message(message: Dict[str, Any], value: Dict[str, Any]) -> NormalizedMessage:
    """
    Normalize WhatsApp message to standard format.
    
    Args:
        message: Message object from webhook
        value: Value object containing metadata
        
    Returns:
        NormalizedMessage with standardized format
    """
    # Extract sender phone number
    sender = message.get("from", "")
    if not sender.startswith("+"):
        sender = f"+{sender}"
    
    # Extract message content based on type
    message_type = message.get("type", "text")
    message_text = ""
    
    if message_type == "text":
        message_text = message.get("text", {}).get("body", "")
    elif message_type == "image":
        message_text = f"[Image] {message.get('image', {}).get('caption', '')}"
    elif message_type == "audio":
        message_text = "[Audio message]"
    elif message_type == "video":
        message_text = "[Video message]"
    elif message_type == "document":
        message_text = "[Document]"
    else:
        message_text = f"[{message_type} message]"
    
    # Get timestamp
    timestamp = datetime.fromtimestamp(int(message.get("timestamp", 0))).isoformat()
    
    return NormalizedMessage(
        channel="whatsapp",
        sender=sender,
        message=message_text,
        timestamp=timestamp,
        message_id=message.get("id"),
        message_type=message_type
    )


@app.post("/send/whatsapp", response_model=SendMessageResponse)
async def send_message(request: SendMessageRequest):
    """
    Endpoint to send WhatsApp messages.
    
    Supports sending text messages and images.
    """
    logger.info(f"Send message request for {request.to}")
    
    try:
        if request.message_type == "text":
            result = await whatsapp_client.send_text_message(
                to=request.to,
                message=request.message
            )
        elif request.message_type == "image":
            if not request.media_url:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="media_url is required for image messages"
                )
            result = await whatsapp_client.send_image_message(
                to=request.to,
                image_url=request.media_url,
                caption=request.message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported message type: {request.message_type}"
            )
        
        if result["success"]:
            message_id = result.get("data", {}).get("messages", [{}])[0].get("id")
            return SendMessageResponse(
                success=True,
                message_id=message_id,
                details=result.get("data")
            )
        else:
            return SendMessageResponse(
                success=False,
                error=str(result.get("error")),
                details=result
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in send_message endpoint: {str(e)}", exc_info=True)
        return SendMessageResponse(
            success=False,
            error=str(e)
        )


async def forward_to_core(normalized_message: NormalizedMessage):
    """Forward normalized message to core API."""
    import httpx
    
    core_url = settings.core_api_url
    
    unified_message = {
        "channel": normalized_message.channel,
        "sender": normalized_message.sender,
        "message": normalized_message.message,
        "timestamp": normalized_message.timestamp,
        "message_id": normalized_message.message_id,
        "message_type": normalized_message.message_type
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(core_url, json=unified_message)
            if response.status_code == 200:
                logger.info("✅ Message forwarded to core successfully")
                print("✅ Message forwarded to core successfully")
            else:
                logger.error(f"❌ Failed to forward to core: {response.status_code}")
                print(f"❌ Failed to forward to core: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Error forwarding to core: {str(e)}")
        print(f"❌ Error forwarding to core: {str(e)}")


async def send_auto_reply(to: str, received_message: str):
    """
    Example function to send an automatic reply.
    
    This is optional and can be used for testing.
    """
    reply = f"Echo: {received_message}"
    await whatsapp_client.send_text_message(to=to, message=reply)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.whatsapp_service:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

