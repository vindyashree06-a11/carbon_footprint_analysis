import os
import logging
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from utils.mongodb import MongoDBManager

# =====================================================
# CONFIGURATION
# =====================================================

load_dotenv()

APP_NAME = "Steel Industry Carbon Footprint & ESG Analytics Platform"

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOGGING
# =====================================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/application.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .metric-card {
        background-color:#111827;
        padding:20px;
        border-radius:15px;
        border:1px solid #374151;
    }

    .title {
        font-size:40px;
        font-weight:bold;
        color:#00d4ff;
    }

    .sub-title {
        font-size:18px;
        color:#9CA3AF;
    }

    footer {
        visibility:hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SESSION STATE
# =====================================================

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

if "dataset" not in st.session_state:
    st.session_state.dataset = None

if "model_trained" not in st.session_state:
    st.session_state.model_trained = False

if "mongo_connected" not in st.session_state:
    st.session_state.mongo_connected = False

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.image(
        "assets/logo.png",
        width="stretch"
    )

    st.markdown("## ESG Intelligence Platform")

    st.divider()

    st.write(
        f"""
        **Version:** 2.0 Enterprise

        **Modules:**
        - Carbon Analytics
        - ESG Compliance
        - Forecasting
        - AutoML
        - Digital Twin
        - Monte Carlo
        - Future Scenario Lab
        """
    )

    st.divider()

    st.write(
        f"Server Time:\n\n{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

# =====================================================
# MONGODB CONNECTION
# =====================================================

@st.cache_resource
def initialize_database():

    try:

        mongo = MongoDBManager()

        # Verify actual Atlas connection
        mongo.client.admin.command("ping")

        st.session_state.mongo_connected = True

        logger.info("MongoDB Connected Successfully")

        return mongo

    except Exception as e:

        logger.error(f"MongoDB Error: {e}")

        st.session_state.mongo_connected = False

        return None


mongo = initialize_database()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div class="title">
    🏭 Steel Industry Carbon Footprint &
    ESG Analytics Platform
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="sub-title">
    AI-Powered Carbon Forecasting, ESG Intelligence,
    Digital Twin Simulation & Sustainability Analytics
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# =====================================================
# SYSTEM STATUS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "MongoDB",
        "Connected"
        if st.session_state.mongo_connected
        else "Offline"
    )

with col2:

   st.metric(
    "Dataset",
    "Loaded"
    if st.session_state.dataset is not None
    else "Not Loaded"
   )

with col3:

 st.metric(
    "Model",
    "Ready"
    if os.path.exists(
        "models/best_carbon_model.pkl"
    )
    else "Not Trained"
)

with col4:

    st.metric(
        "Platform",
        "Enterprise"
    )

# =====================================================
# DATA UPLOAD
# =====================================================

st.subheader("📂 Upload Steel Industry Dataset")

uploaded_file = st.file_uploader(
    "Upload Steel_industry_data.csv",
    type=["csv"]
)

if uploaded_file:

    try:

        import pandas as pd

        df = pd.read_csv(uploaded_file)

        st.session_state.dataset = df

        st.session_state.data_loaded = True

        st.success(
            f"Dataset Loaded Successfully ({df.shape[0]} rows)"
        )

       if mongo and hasattr(
    mongo,
    "insert_dataset_log"
):

    try:

        mongo.insert_dataset_log(
            {
                "filename": uploaded_file.name,
                "rows": int(df.shape[0]),
                "columns": int(df.shape[1]),
                "upload_time": datetime.utcnow()
            }
        )

    except Exception as e:

        logger.error(
            f"Dataset Log Error: {e}"
        )
        logger.info(
            f"Dataset Uploaded: {uploaded_file.name}"
        )

    except Exception as e:

        st.error(str(e))

        logger.exception(e)

# =====================================================
# DATA PREVIEW
# =====================================================

if st.session_state.data_loaded:

    st.subheader("Dataset Preview")

    st.dataframe(
        st.session_state.dataset.head(),
       width="stretch"
    )

    rows = st.session_state.dataset.shape[0]
    cols = st.session_state.dataset.shape[1]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Rows",
            rows
        )

    with col2:

        st.metric(
            "Columns",
            cols
        )

# =====================================================
# PLATFORM FEATURES
# =====================================================

st.divider()

st.subheader("🚀 Platform Modules")

c1, c2, c3 = st.columns(3)

with c1:

    st.info(
        """
        ### Carbon Analytics

        • Emission Tracking

        • Carbon Intensity

        • Load Type Analysis

        • Trend Monitoring
        """
    )

with c2:

    st.info(
        """
        ### Forecasting Engine

        • Prophet

        • SARIMA

        • XGBoost

        • LightGBM

        • AutoML
        """
    )

with c3:

    st.info(
        """
        ### ESG Intelligence

        • ESG Score

        • Compliance Engine

        • Sustainability Rating

        • Recommendations
        """
    )

# =====================================================
# NEW ENTERPRISE MODULES
# =====================================================

st.subheader("🧠 Enterprise AI Modules")

col1, col2, col3 = st.columns(3)

with col1:

    st.success(
        """
        Future Scenario Lab

        Digital Twin

        What-If Analysis
        """
    )

with col2:

    st.success(
        """
        Monte Carlo Simulation

        Risk Assessment

        Carbon Budget Tracking
        """
    )

with col3:

    st.success(
        """
        AutoML Engine

        Model Comparison

        Forecast Intelligence
        """
    )

# =====================================================
# NAVIGATION GUIDE
# =====================================================

st.divider()

st.subheader("📊 Dashboard Navigation")

st.markdown(
    """
### Available Pages

1. Executive Summary

2. Carbon Analytics

3. Prediction Center

4. ESG Dashboard

5. Load Analysis

6. Anomaly Detection Center

7. Sustainability Insights

8. Future Scenario Lab

9. Model Comparison Center

Use the left sidebar to navigate between pages.
"""
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    """
Steel Industry Carbon Footprint &
ESG Analytics Platform v2.0 Enterprise

Built with:

Streamlit • Scikit-Learn • XGBoost • LightGBM
• CatBoost • Prophet • MongoDB Atlas • Plotly
"""
)

logger.info("Application Loaded Successfully")
