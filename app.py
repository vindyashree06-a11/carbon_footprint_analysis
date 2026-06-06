import os
import logging
from datetime import datetime

import streamlit as st
import pandas as pd
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

st.markdown("""
<style>

.main {
    padding-top: 1rem;
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
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "dataset" not in st.session_state:
    st.session_state.dataset = None

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

if "mongo_connected" not in st.session_state:
    st.session_state.mongo_connected = False

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    if os.path.exists("assets/logo.png"):
        st.image(
            "assets/logo.png",
            use_container_width=True
        )

    st.markdown("## ESG Intelligence Platform")

    st.divider()

    st.write("""
    **Version:** 2.0 Enterprise

    **Modules**
    - Carbon Analytics
    - ESG Compliance
    - Forecasting
    - AutoML
    - Digital Twin
    - Monte Carlo
    - Future Scenario Lab
    """)

    st.divider()

    st.write(
        f"Server Time:\n\n{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

# =====================================================
# DATABASE
# =====================================================

@st.cache_resource
def initialize_database():

    try:

        mongo = MongoDBManager()

        mongo.client.admin.command("ping")

        st.session_state.mongo_connected = True

        logger.info("MongoDB Connected")

        return mongo

    except Exception as e:

        st.error(f"MongoDB Connection Failed: {e}")

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
    🏭 Steel Industry Carbon Footprint & ESG Analytics Platform
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
# STATUS CARDS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "MongoDB",
        "Connected" if st.session_state.mongo_connected else "Offline"
    )

with c2:
    st.metric(
        "Dataset",
        "Loaded" if st.session_state.dataset is not None else "Not Loaded"
    )

with c3:
    st.metric(
        "Model",
        "Ready"
        if os.path.exists("models/best_carbon_model.pkl")
        else "Not Trained"
    )

with c4:
    st.metric(
        "Platform",
        "Enterprise"
    )

# =====================================================
# FILE UPLOAD
# =====================================================

st.subheader("📂 Upload Steel Industry Dataset")

uploaded_file = st.file_uploader(
    "Upload Steel_industry_data.csv",
    type=["csv"]
)

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        st.session_state.dataset = df
        st.session_state.data_loaded = True

        st.success(
            f"Dataset Loaded Successfully ({len(df)} rows)"
        )

        if mongo:

            try:

                mongo.insert_dataset_log(
                    {
                        "filename": uploaded_file.name,
                        "rows": int(df.shape[0]),
                        "columns": int(df.shape[1]),
                        "upload_time": datetime.utcnow()
                    }
                )

            except Exception as mongo_error:

                logger.error(
                    f"MongoDB Logging Error: {mongo_error}"
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

if st.session_state.dataset is not None:

    st.subheader("Dataset Preview")

    st.dataframe(
        st.session_state.dataset.head(),
        use_container_width=True
    )

    rows = st.session_state.dataset.shape[0]
    cols = st.session_state.dataset.shape[1]

    a, b = st.columns(2)

    with a:
        st.metric("Rows", rows)

    with b:
        st.metric("Columns", cols)

# =====================================================
# PLATFORM MODULES
# =====================================================

st.divider()

st.subheader("🚀 Platform Modules")

c1, c2, c3 = st.columns(3)

with c1:

    st.info("""
### Carbon Analytics

• Emission Tracking

• Carbon Intensity

• Load Analysis

• Trend Monitoring
""")

with c2:

    st.info("""
### Forecasting Engine

• Prophet

• SARIMA

• XGBoost

• LightGBM

• AutoML
""")

with c3:

    st.info("""
### ESG Intelligence

• ESG Score

• Compliance Engine

• Sustainability Rating

• Recommendations
""")

# =====================================================
# ENTERPRISE MODULES
# =====================================================

st.subheader("🧠 Enterprise AI Modules")

e1, e2, e3 = st.columns(3)

with e1:
    st.success("""
Future Scenario Lab

Digital Twin

What-If Analysis
""")

with e2:
    st.success("""
Monte Carlo Simulation

Risk Assessment

Carbon Budget Tracking
""")

with e3:
    st.success("""
AutoML Engine

Model Comparison

Forecast Intelligence
""")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption("""
Steel Industry Carbon Footprint & ESG Analytics Platform v2.0 Enterprise

Built with:

Streamlit • Scikit-Learn • XGBoost • LightGBM
• CatBoost • Prophet • MongoDB Atlas • Plotly
""")

logger.info("Application Loaded Successfully")
