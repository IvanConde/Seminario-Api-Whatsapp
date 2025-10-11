"""Basic tests for WhatsApp service."""
import pytest
from fastapi.testclient import TestClient
from src.whatsapp_service import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "WhatsApp Integration Service"


def test_webhook_verification_success():
    """Test successful webhook verification."""
    response = client.get(
        "/webhook/whatsapp",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "my_verify_token_123",
            "hub.challenge": "test_challenge_123"
        }
    )
    assert response.status_code == 200
    assert response.text == "test_challenge_123"


def test_webhook_verification_failure():
    """Test webhook verification with wrong token."""
    response = client.get(
        "/webhook/whatsapp",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "wrong_token",
            "hub.challenge": "test_challenge_123"
        }
    )
    assert response.status_code == 403


def test_webhook_receive_message():
    """Test receiving a webhook message."""
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "123456",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "15551234567",
                        "phone_number_id": "PHONE_ID"
                    },
                    "contacts": [{
                        "profile": {"name": "Test User"},
                        "wa_id": "5491112345678"
                    }],
                    "messages": [{
                        "from": "5491112345678",
                        "id": "wamid.test123",
                        "timestamp": "1633024800",
                        "text": {"body": "Hola"},
                        "type": "text"
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    
    response = client.post("/webhook/whatsapp", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

