import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path

from from_root import from_root

# Constants for log configuration
# - LOG_PATH (full file path) overrides everything
# - LOG_DIR is interpreted relative to the project root unless it's absolute
# - LOG_FILE defaults to a timestamped filename
LOG_DIR = os.getenv('LOG_DIR', 'logs')
LOG_FILE = os.getenv('LOG_FILE', f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log")
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Number of backup log files to keep

# Determine project root (via from_root)
_PROJECT_ROOT = Path(from_root())

# Allow overriding the log location via environment variables
LOG_PATH = os.getenv('LOG_PATH')
if LOG_PATH:
    log_file_path = Path(LOG_PATH)
else:
    log_dir_path = Path(LOG_DIR)
    if not log_dir_path.is_absolute():
        log_dir_path = _PROJECT_ROOT / log_dir_path
    log_dir_path.mkdir(parents=True, exist_ok=True)
    log_file_path = log_dir_path / LOG_FILE

def configure_logger():
    """
    Configures logging with a rotating file handler and a console handler.
    """
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Define formatter
    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    # File handler with rotation
    file_handler = RotatingFileHandler(log_file_path, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Configure the logger
configure_logger()