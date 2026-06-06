
"""
logger.py
Centralized logging utility for the
Steel Industry Carbon Footprint & ESG Analytics Platform
"""

import os
import logging
from logging.handlers import RotatingFileHandler


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "application.log")

os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name: str = "steel_esg"):
    """
    Returns a configured logger instance.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False

    return logger


# Example Usage
if __name__ == "__main__":

    log = get_logger("test")

    log.info("Logger initialized")
    log.warning("Warning message")
    log.error("Error message")
