"""Configuration management for WhatsApp service."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # WhatsApp API Configuration
    whatsapp_access_token: str = "DEMO_TOKEN"
    whatsapp_phone_number_id: str = "DEMO_PHONE_ID"
    whatsapp_verify_token: str = "my_verify_token_123"
    whatsapp_business_account_id: str = "DEMO_BUSINESS_ID"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Logging
    log_level: str = "INFO"
    
    # WhatsApp API Base URL
    whatsapp_api_base_url: str = "https://graph.facebook.com/v18.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

