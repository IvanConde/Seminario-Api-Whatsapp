"""Logging configuration for WhatsApp service."""
import logging
import sys
from pathlib import Path
from datetime import datetime
from src.config import settings


# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logging format
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

# Create formatters
formatter = logging.Formatter(log_format, datefmt=date_format)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, settings.log_level))
console_handler.setFormatter(formatter)

# File handler (daily log file)
log_filename = logs_dir / f"whatsapp_service_{datetime.now().strftime('%Y%m%d')}.log"
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Configure root logger
logger = logging.getLogger("whatsapp_service")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Prevent duplicate logs
logger.propagate = False


def get_logger(name: str = "whatsapp_service") -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)

