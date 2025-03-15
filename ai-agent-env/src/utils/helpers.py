import logging
import time
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def log_message(message, level="info"):
    """
    Log a message with a specified log level.
    """
    if level.lower() == "info":
        logger.info(message)
    elif level.lower() == "warning":
        logger.warning(message)
    elif level.lower() == "error":
        logger.error(message)
    elif level.lower() == "debug":
        logger.debug(message)
    else:
        logger.info(message)  # Default to info

def retry_on_failure(func, max_retries=3, delay=5):
    """
    Retry a function if it fails.
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            log_message(f"Attempt {attempt + 1} failed: {e}", level="warning")
            time.sleep(delay)
    raise Exception(f"Function failed after {max_retries} attempts")

def format_timestamp(timestamp):
    """
    Format a timestamp into a human-readable string.
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def validate_wallet_address(address):
    """
    Validate an Ethereum wallet address.
    """
    if not address.startswith("0x") or len(address) != 42:
        raise ValueError("Invalid Ethereum wallet address")
    return True

def validate_token_amount(amount):
    """
    Validate a token amount (must be a positive number).
    """
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Token amount must be a positive number")
    return True