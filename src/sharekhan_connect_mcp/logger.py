"""
Logging configuration for Sharekhan MCP Server
"""

import sys
from pathlib import Path
from loguru import logger
from .config import Settings

def setup_logging(settings: Settings) -> logger:
    """Setup structured logging with loguru"""

    # Remove default handler
    logger.remove()

    # Ensure log directory exists
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Console handler with formatting
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True
    )

    # File handler for persistent logs
    logger.add(
        settings.log_file,
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        serialize=False  # Set to True for JSON structured logging
    )

    return logger
