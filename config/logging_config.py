"""
====================================================
Steel Industry Carbon Footprint & ESG Platform
logging_config.py
====================================================

Centralized Logging Configuration

Features:
---------
✔ Console Logging
✔ File Logging
✔ Rotating Logs
✔ Error Logs
✔ Production Ready
✔ Streamlit Compatible

Author: Enterprise ESG Platform
Version: 2.0
====================================================
"""

import logging
import logging.handlers
from pathlib import Path

from config.settings import (
    LOG_DIR,
    LOG_LEVEL,
    LOG_FORMAT
)

# ====================================================
# CREATE LOG DIRECTORY
# ====================================================

Path(LOG_DIR).mkdir(
    parents=True,
    exist_ok=True
)

# ====================================================
# LOG FILES
# ====================================================

APPLICATION_LOG = Path(LOG_DIR) / "application.log"

ERROR_LOG = Path(LOG_DIR) / "errors.log"

# ====================================================
# FORMATTER
# ====================================================

formatter = logging.Formatter(LOG_FORMAT)

# ====================================================
# ROOT LOGGER
# ====================================================

root_logger = logging.getLogger()

root_logger.setLevel(
    getattr(logging, LOG_LEVEL.upper(), logging.INFO)
)

# Prevent duplicate handlers

if root_logger.handlers:
    root_logger.handlers.clear()

# ====================================================
# CONSOLE HANDLER
# ====================================================

console_handler = logging.StreamHandler()

console_handler.setLevel(
    getattr(logging, LOG_LEVEL.upper(), logging.INFO)
)

console_handler.setFormatter(formatter)

root_logger.addHandler(console_handler)

# ====================================================
# APPLICATION LOG ROTATION
# ====================================================

app_handler = logging.handlers.RotatingFileHandler(
    APPLICATION_LOG,
    maxBytes=10 * 1024 * 1024,   # 10 MB
    backupCount=5,
    encoding="utf-8"
)

app_handler.setLevel(logging.INFO)

app_handler.setFormatter(formatter)

root_logger.addHandler(app_handler)

# ====================================================
# ERROR LOG ROTATION
# ====================================================

error_handler = logging.handlers.RotatingFileHandler(
    ERROR_LOG,
    maxBytes=5 * 1024 * 1024,    # 5 MB
    backupCount=3,
    encoding="utf-8"
)

error_handler.setLevel(logging.ERROR)

error_handler.setFormatter(formatter)

root_logger.addHandler(error_handler)

# ====================================================
# LOGGER FACTORY
# ====================================================

def get_logger(name: str) -> logging.Logger:
    """
    Returns configured logger.

    Example:
    --------
    logger = get_logger(__name__)
    """

    logger = logging.getLogger(name)

    logger.setLevel(
        getattr(
            logging,
            LOG_LEVEL.upper(),
            logging.INFO
        )
    )

    return logger

# ====================================================
# APPLICATION LOGGER
# ====================================================

logger = get_logger("steel_esg")

# ====================================================
# STARTUP MESSAGE
# ====================================================

logger.info("=" * 60)
logger.info("Steel Industry ESG Platform Started")
logger.info("Logging System Initialized")
logger.info("=" * 60)

# ====================================================
# LOGGING HELPERS
# ====================================================

def log_info(message: str):
    """
    Log info message.
    """
    logger.info(message)


def log_warning(message: str):
    """
    Log warning message.
    """
    logger.warning(message)


def log_error(message: str):
    """
    Log error message.
    """
    logger.error(message)


def log_exception(exception: Exception):
    """
    Log exception with traceback.
    """
    logger.exception(exception)

# ====================================================
# STREAMLIT EVENT LOGGING
# ====================================================

def log_page_visit(page_name: str):
    """
    Log page visits.
    """

    logger.info(
        f"PAGE_VISIT | {page_name}"
    )


def log_dataset_upload(
    filename: str,
    rows: int,
    columns: int
):
    """
    Log uploaded dataset metadata.
    """

    logger.info(
        f"DATASET_UPLOAD | "
        f"File={filename} | "
        f"Rows={rows} | "
        f"Columns={columns}"
    )


def log_model_training(
    model_name: str,
    score: float
):
    """
    Log model training results.
    """

    logger.info(
        f"MODEL_TRAINED | "
        f"Model={model_name} | "
        f"Score={score:.4f}"
    )


def log_prediction(
    model_name: str,
    prediction
):
    """
    Log prediction event.
    """

    logger.info(
        f"PREDICTION | "
        f"Model={model_name} | "
        f"Value={prediction}"
    )


def log_forecast(
    model_name: str,
    horizon: int
):
    """
    Log forecast generation.
    """

    logger.info(
        f"FORECAST | "
        f"Model={model_name} | "
        f"Horizon={horizon}"
    )


def log_scenario(
    scenario_name: str
):
    """
    Log Future Scenario Lab simulations.
    """

    logger.info(
        f"SCENARIO_RUN | "
        f"{scenario_name}"
    )


def log_monte_carlo(
    iterations: int
):
    """
    Log Monte Carlo execution.
    """

    logger.info(
        f"MONTE_CARLO | "
        f"Iterations={iterations}"
    )


def log_esg_score(
    score: float
):
    """
    Log ESG score calculations.
    """

    logger.info(
        f"ESG_SCORE | "
        f"Score={score:.2f}"
    )

# ====================================================
# HEALTH CHECK
# ====================================================

def test_logging():
    """
    Test logging configuration.
    """

    logger.info("Logging test successful")
    logger.warning("Warning test successful")

    try:
        1 / 0
    except Exception as e:
        logger.exception(e)

# ====================================================
# MAIN TEST
# ====================================================

if __name__ == "__main__":

    test_logging()
