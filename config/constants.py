"""
====================================================
Steel Industry Carbon Footprint & ESG Platform
constants.py
====================================================

Centralized Constants

Author: Enterprise ESG Platform
Version: 2.0
====================================================
"""

# ====================================================
# DATASET COLUMNS
# ====================================================

USAGE_KWH = "Usage_kWh"

LAGGING_REACTIVE_POWER = (
    "Lagging_Current_Reactive.Power_kVarh"
)

LEADING_REACTIVE_POWER = (
    "Leading_Current_Reactive_Power_kVarh"
)

CO2_COLUMN = "CO2(tCO2)"

LAGGING_POWER_FACTOR = (
    "Lagging_Current_Power_Factor"
)

LEADING_POWER_FACTOR = (
    "Leading_Current_Power_Factor"
)

NSM_COLUMN = "NSM"

WEEK_STATUS = "WeekStatus"

DAY_OF_WEEK = "Day_of_week"

LOAD_TYPE = "Load_Type"

DATE_COLUMN = "Date"

# ====================================================
# FEATURE ENGINEERING
# ====================================================

TOTAL_POWER_CONSUMPTION = (
    "Total_Power_Consumption"
)

REACTIVE_POWER_RATIO = (
    "Reactive_Power_Ratio"
)

CARBON_INTENSITY = (
    "Carbon_Intensity"
)

ROLLING_7_DAY_EMISSION = (
    "Rolling_7_Day_Emission"
)

ROLLING_30_DAY_EMISSION = (
    "Rolling_30_Day_Emission"
)

ENERGY_EFFICIENCY_INDEX = (
    "Energy_Efficiency_Index"
)

PEAK_LOAD_FLAG = (
    "Peak_Load_Flag"
)

WEEKEND_FLAG = (
    "Weekend_Flag"
)

SEASONAL_USAGE_INDEX = (
    "Seasonal_Usage_Index"
)

LOAD_TYPE_ENCODING = (
    "Load_Type_Encoding"
)

# ====================================================
# FUTURE SCENARIO FEATURES
# ====================================================

FUTURE_USAGE = "Future_Usage_kWh"

FUTURE_REACTIVE_POWER = (
    "Future_Reactive_Power"
)

FUTURE_POWER_FACTOR = (
    "Future_Power_Factor"
)

FUTURE_LOAD_INDEX = (
    "Future_Load_Index"
)

RENEWABLE_ADJUSTMENT = (
    "Renewable_Adjustment"
)

OPTIMIZATION_SCORE = (
    "Optimization_Score"
)

MAINTENANCE_SCORE = (
    "Maintenance_Score"
)

PROJECTED_CARBON_INTENSITY = (
    "Projected_Carbon_Intensity"
)

PROJECTED_ESG_SCORE = (
    "Projected_ESG_Score"
)

PROJECTED_ENERGY_EFFICIENCY = (
    "Projected_Energy_Efficiency"
)

# ====================================================
# LOAD TYPES
# ====================================================

LIGHT_LOAD = "Light Load"

MEDIUM_LOAD = "Medium Load"

MAXIMUM_LOAD = "Maximum Load"

LOAD_TYPES = [
    LIGHT_LOAD,
    MEDIUM_LOAD,
    MAXIMUM_LOAD
]

LOAD_TYPE_MAPPING = {
    LIGHT_LOAD: 0,
    MEDIUM_LOAD: 1,
    MAXIMUM_LOAD: 2
}

# ====================================================
# DAYS
# ====================================================

DAYS_OF_WEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

# ====================================================
# WEEK STATUS
# ====================================================

WORKING_DAY = "Weekday"

WEEKEND = "Weekend"

# ====================================================
# FORECAST HORIZONS
# ====================================================

FORECAST_1_DAY = 1

FORECAST_7_DAYS = 7

FORECAST_30_DAYS = 30

FORECAST_90_DAYS = 90

FORECAST_180_DAYS = 180

FORECAST_365_DAYS = 365

FORECAST_OPTIONS = [
    30,
    90,
    180,
    365
]

# ====================================================
# ESG STATUS
# ====================================================

ESG_GREEN = "Green"

ESG_YELLOW = "Yellow"

ESG_RED = "Red"

ESG_STATUSES = [
    ESG_GREEN,
    ESG_YELLOW,
    ESG_RED
]

# ====================================================
# ALERT LEVELS
# ====================================================

LOW_ALERT = "LOW"

MEDIUM_ALERT = "MEDIUM"

HIGH_ALERT = "HIGH"

CRITICAL_ALERT = "CRITICAL"

ALERT_LEVELS = [
    LOW_ALERT,
    MEDIUM_ALERT,
    HIGH_ALERT,
    CRITICAL_ALERT
]

# ====================================================
# ANOMALY TYPES
# ====================================================

USAGE_SPIKE = (
    "Usage_kWh_Spike"
)

EMISSION_SPIKE = (
    "CO2_Emission_Spike"
)

POWER_FACTOR_ANOMALY = (
    "Power_Factor_Anomaly"
)

REACTIVE_POWER_ANOMALY = (
    "Reactive_Power_Anomaly"
)

LOAD_PATTERN_DEVIATION = (
    "Load_Pattern_Deviation"
)

# ====================================================
# SUPPORTED ML MODELS
# ====================================================

MODEL_LINEAR = "Linear Regression"

MODEL_RIDGE = "Ridge Regression"

MODEL_LASSO = "Lasso Regression"

MODEL_ELASTICNET = "ElasticNet"

MODEL_RF = "Random Forest"

MODEL_EXTRA_TREES = "Extra Trees"

MODEL_GB = "Gradient Boosting"

MODEL_ADABOOST = "AdaBoost"

MODEL_HGB = (
    "HistGradientBoosting"
)

MODEL_XGB = "XGBoost"

MODEL_LGBM = "LightGBM"

MODEL_CATBOOST = "CatBoost"

REGRESSION_MODELS = [
    MODEL_LINEAR,
    MODEL_RIDGE,
    MODEL_LASSO,
    MODEL_ELASTICNET,
    MODEL_RF,
    MODEL_EXTRA_TREES,
    MODEL_GB,
    MODEL_ADABOOST,
    MODEL_HGB,
    MODEL_XGB,
    MODEL_LGBM,
    MODEL_CATBOOST
]

# ====================================================
# TIME SERIES MODELS
# ====================================================

PROPHET_MODEL = "Prophet"

SARIMA_MODEL = "SARIMA"

EXPONENTIAL_MODEL = (
    "ExponentialSmoothing"
)

RF_TS_MODEL = (
    "RandomForest_TS"
)

XGB_TS_MODEL = (
    "XGBoost_TS"
)

LGBM_TS_MODEL = (
    "LightGBM_TS"
)

TIME_SERIES_MODELS = [
    PROPHET_MODEL,
    SARIMA_MODEL,
    EXPONENTIAL_MODEL,
    RF_TS_MODEL,
    XGB_TS_MODEL,
    LGBM_TS_MODEL
]

# ====================================================
# MONGODB COLLECTIONS
# ====================================================

COLLECTION_DATASET_LOGS = (
    "dataset_logs"
)

COLLECTION_EMISSIONS = (
    "emissions"
)

COLLECTION_PREDICTIONS = (
    "predictions"
)

COLLECTION_ALERTS = (
    "alerts"
)

COLLECTION_ESG_REPORTS = (
    "esg_reports"
)

COLLECTION_INSIGHTS = (
    "insights"
)

COLLECTION_FUTURE_SCENARIOS = (
    "future_scenarios"
)

COLLECTION_FORECASTS = (
    "forecasts"
)

COLLECTION_MODEL_SCORES = (
    "model_scores"
)

COLLECTION_SIMULATION_RESULTS = (
    "simulation_results"
)

COLLECTION_DIGITAL_TWIN = (
    "digital_twin"
)

# ====================================================
# KPI LABELS
# ====================================================

TOTAL_EMISSIONS = (
    "Total Emissions"
)

AVERAGE_DAILY_EMISSIONS = (
    "Average Daily Emissions"
)

ENERGY_CONSUMPTION = (
    "Energy Consumption"
)

CARBON_INTENSITY_KPI = (
    "Carbon Intensity"
)

ESG_SCORE_KPI = (
    "ESG Score"
)

ACTIVE_ALERTS = (
    "Active Alerts"
)

# ====================================================
# COLORS
# ====================================================

PRIMARY_COLOR = "#00D4FF"

SUCCESS_COLOR = "#22C55E"

WARNING_COLOR = "#FACC15"

DANGER_COLOR = "#EF4444"

INFO_COLOR = "#3B82F6"

BACKGROUND_COLOR = "#0E1117"

CARD_COLOR = "#1E293B"

TEXT_COLOR = "#FAFAFA"

# ====================================================
# CHART THEMES
# ====================================================

PLOTLY_THEME = "plotly_dark"

DEFAULT_HEIGHT = 500

DEFAULT_WIDTH = 1200

# ====================================================
# FILE EXTENSIONS
# ====================================================

CSV = ".csv"

XLSX = ".xlsx"

PARQUET = ".parquet"

SUPPORTED_UPLOADS = [
    CSV,
    XLSX
]

# ====================================================
# MISC
# ====================================================

RANDOM_STATE = 42

DEFAULT_PORT = 8501

APP_VERSION = "2.0 Enterprise"

APP_AUTHOR = (
    "Steel ESG Intelligence Platform"
)
