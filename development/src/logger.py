"""Logging setup for BlackDuck AI Command"""

import os
import sys
from pathlib import Path
from loguru import logger

# Remove default handler
logger.remove()

# Get configuration from environment
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Ensure logs directory exists
logs_dir = Path(__file__).parent.parent / "logs"
logs_dir.mkdir(exist_ok=True)

# Configure console handler (always)
logger.add(
    sys.stdout,
    level="DEBUG" if DEBUG else LOG_LEVEL,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    colorize=True,
)

# Configure file handler
logger.add(
    str(logs_dir / "app.log"),
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="10 MB",
    retention="1 week",
)


def get_logger(name: str):
    """Get a logger instance with the given name"""
    return logger.bind(name=name)
