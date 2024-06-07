import logging
import os
from datetime import datetime

def setup_logging():
    logger = logging.getLogger("app")  # Changed from "myapp" to "app"
    logger.setLevel(logging.INFO)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Check if logs directory exists, if not, create it
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # File Handler
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_handler = logging.FileHandler(f'logs/app_{timestamp}.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger