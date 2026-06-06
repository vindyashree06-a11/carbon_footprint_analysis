"""
====================================================
Steel Industry Carbon Footprint & ESG Platform
settings.py
====================================================

Centralized Application Configuration

Author: Enterprise ESG Analytics Platform
Version: 2.0
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ====================================================
# LOAD ENVIRONMENT VARIABLES
# ====================================================

load_dotenv()

# ====================================================
# ROOT PATHS
# ====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

MODEL_DIR = BASE_DIR / "models"

LOG_DIR = BASE_DIR / "logs"

ASSETS_DIR = BASE_DIR / "assets"

CONFIG_DIR = BASE_DIR / "config"

# Create folders automatically

DATA_DIR.mkdir(exist_ok=True)

MODEL_DIR.mkdir(exist_ok=True)

LOG_DIR.mkdir(exist_ok=True)

# ====================================================
# APPLICATION SETTINGS
# ====================================================

APP_NAME = "Steel Industry Carbon Footprint & ESG Analytics Platform"

APP_VERSION = "2.0 Enterprise"

COMPANY_NAME = "Steel ESG Intelligence Suite"

DEFAULT_PAGE = "Executive Summary"

DATE_FORMAT = "%Y-%m-%d"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# ====================================================
# STREAMLIT SETTINGS
# ====================================================

PAGE_TITLE = APP_NAME

PAGE_ICON = "🏭"

LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

# ====================================================
# MONGODB SETTINGS
# ====================================================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

DATABASE_NAME = os.getenv(
    "DB_NAME",
    "steel_esg"
)

# Collections

DATASET_COLLECTION = "dataset_logs"

EMISSIONS_COLLECTION = "emissions"

PREDICTIONS_COLLECTION = "predictions"

ALERTS_COLLECTION = "alerts"

ESG_COLLECTION = "esg_reports"

INSIGHTS_COLLECTION = "insights"

FUTURE_SCENARIO_COLLECTION = "future_scenarios"

FORECAST_COLLECTION = "forecasts"

MODEL_SCORES_COLLECTION = "model_scores"

SIMULATION_COLLECTION = "simulation_results"

DIGITAL_TWIN_COLLECTION = "digital_twin"

# ====================================================
# MODEL PATHS
# ====================================================

CARBON_MODEL_PATH = MODEL_DIR / "carbon_model.pkl"

BEST_MODEL_PATH = MODEL_DIR / "best_carbon_model.pkl"

PROPHET_MODEL_PATH = MODEL_DIR / "prophet_model.pkl"

SARIMA_MODEL_PATH = MODEL_DIR / "sarima_model.pkl"

AUTOML_RESULTS_PATH = MODEL_DIR / "automl_results.pkl"

# ====================================================
# MACHINE LEARNING SETTINGS
# ====================================================

RANDOM_STATE = 42

TEST_SIZE = 0.20

CV_FOLDS = 5

N_JOBS = -1

# ====================================================
# AUTOML SETTINGS
# ====================================================

ENABLE_AUTOML = True

GRID_SEARCH_JOBS = -1

RANDOM_SEARCH_ITERATIONS = 20

MODEL_SELECTION_METRIC = "weighted_score"

# Weighted Ranking Formula

WEIGHT_R2 = 0.40

WEIGHT_RMSE = 0.30

WEIGHT_MAE = 0.20

WEIGHT_STABILITY = 0.10

# ====================================================
# FORECAST SETTINGS
# ====================================================

FORECAST_DAYS = 30

FORECAST_QUARTER = 90

FORECAST_HALF_YEAR = 180

FORECAST_YEAR = 365

ENABLE_PROPHET = True

ENABLE_SARIMA = True

ENABLE_EXP_SMOOTHING = True

ENABLE_RF_FORECAST = True

ENABLE_XGB_FORECAST = True

ENABLE_LGBM_FORECAST = True

# ====================================================
# MONTE CARLO SETTINGS
# ====================================================

ENABLE_MONTE_CARLO = True

SIMULATION_RUNS = 1000

DEFAULT_CONFIDENCE = 95

MONTE_CARLO_STD = 0.10

# ====================================================
# ESG TARGET SETTINGS
# ====================================================

TARGET_REDUCTION_PERCENT = 20

TARGET_CARBON_INTENSITY = 0.80

TARGET_ESG_SCORE = 85

# ESG Status

ESG_GREEN_THRESHOLD = 85

ESG_YELLOW_THRESHOLD = 65

ESG_RED_THRESHOLD = 40

# ====================================================
# ANOMALY DETECTION
# ====================================================

ISOLATION_FOREST_CONTAMINATION = 0.05

ROLLING_MEDIAN_MULTIPLIER = 1.5

ANOMALY_SCORE_THRESHOLD = 0.70

# ====================================================
# FUTURE SCENARIO LAB
# ====================================================

USAGE_CHANGE_MIN = -50

USAGE_CHANGE_MAX = 100

POWER_FACTOR_MIN = -20

POWER_FACTOR_MAX = 20

REACTIVE_POWER_MIN = -50

REACTIVE_POWER_MAX = 50

PRODUCTION_GROWTH_MIN = 0

PRODUCTION_GROWTH_MAX = 100

RENEWABLE_MIN = 0

RENEWABLE_MAX = 100

# ====================================================
# LOAD TYPE ENCODING
# ====================================================

LOAD_TYPE_MAPPING = {
    "Light_Load": 0,
    "Medium_Load": 1,
    "Maximum_Load": 2
}

# ====================================================
# ALERT LEVELS
# ====================================================

ALERT_LEVELS = {
    "LOW": "#22C55E",
    "MEDIUM": "#FACC15",
    "HIGH": "#F97316",
    "CRITICAL": "#EF4444"
}

# ====================================================
# LOGGING
# ====================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

LOG_FILE = LOG_DIR / "application.log"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

# ====================================================
# PLOTLY COLORS
# ====================================================

PRIMARY_COLOR = "#00D4FF"

SUCCESS_COLOR = "#22C55E"

WARNING_COLOR = "#FACC15"

DANGER_COLOR = "#EF4444"

INFO_COLOR = "#3B82F6"

# ====================================================
# CACHE SETTINGS
# ====================================================

CACHE_TTL = 3600

ENABLE_CACHE = True

# ====================================================
# FEATURE ENGINEERING
# ====================================================

ROLLING_WINDOW_7 = 7

ROLLING_WINDOW_30 = 30

PEAK_LOAD_PERCENTILE = 95

# ====================================================
# DIGITAL TWIN
# ====================================================

ENABLE_DIGITAL_TWIN = True

TWIN_REFRESH_SECONDS = 30

# ====================================================
# SECURITY
# ====================================================

MAX_UPLOAD_SIZE_MB = 200

ALLOWED_EXTENSIONS = [
    ".csv",
    ".xlsx"
]

# ====================================================
# DASHBOARD KPI LABELS
# ====================================================

KPI_LABELS = {
    "emissions": "Total Emissions",
    "daily_emission": "Average Daily Emissions",
    "energy": "Energy Consumption",
    "carbon_intensity": "Carbon Intensity",
    "esg_score": "ESG Score",
    "alerts": "Active Alerts"
}

# ====================================================
# STARTUP MESSAGE
# ====================================================

print(
    f"""
====================================================
{APP_NAME}
Version : {APP_VERSION}
Database: {DATABASE_NAME}
====================================================
"""
)
