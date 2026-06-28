import sys
from loguru import logger
from pathlib import Path

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

# Remove default handler to prevent double-logging
logger.remove()

# Add console handler (Colorized for development)
logger.add(
    sys.stderr, 
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# Add offline file handler (Full stack traces for production debugging)
logger.add(
    "logs/chronicle_errors.log", 
    rotation="10 MB", 
    level="ERROR", 
    backtrace=True, 
    diagnose=True
)
