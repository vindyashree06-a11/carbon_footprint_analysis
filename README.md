# 🌍 Steel Industry Carbon Footprint & ESG Analytics Platform

## Overview

The **Steel Industry Carbon Footprint & ESG Analytics Platform** is an enterprise-grade analytics and machine learning application designed to monitor, analyze, predict, and optimize carbon emissions within steel manufacturing operations.

The platform combines:

* Carbon Footprint Analytics
* ESG Compliance Monitoring
* Machine Learning Forecasting
* Energy Consumption Analysis
* Anomaly Detection
* Sustainability Intelligence
* MongoDB Atlas Integration
* Interactive Streamlit Dashboards

The solution enables steel manufacturers to track sustainability performance, reduce emissions, improve energy efficiency, and align with ESG reporting requirements.

---

# Features

## Phase 1 — Data Ingestion

### Upload Dataset

Upload:

```text
Steel_industry_data.csv
```

Supported Columns:

| Column                               |
| ------------------------------------ |
| Usage_kWh                            |
| Lagging_Current_Reactive.Power_kVarh |
| Leading_Current_Reactive_Power_kVarh |
| CO2(tCO2)                            |
| Lagging_Current_Power_Factor         |
| Leading_Current_Power_Factor         |
| NSM                                  |
| WeekStatus                           |
| Day_of_week                          |
| Load_Type                            |
| Date                                 |

### Automated Data Quality Checks

* Missing Value Handling
* Duplicate Detection & Removal
* Data Validation
* Date Parsing
* Data Type Conversion
* Outlier Detection

### Data Summaries

* Dataset Preview
* Descriptive Statistics
* Load Type Summary
* Weekly Usage Summary
* Carbon Emission Summary

---

# Carbon Footprint Analytics

The platform performs advanced emission analysis using:

```text
CO2(tCO2)
```

### Calculations

* Daily Emissions
* Weekly Emissions
* Monthly Emissions
* Annualized Emissions

### KPIs

* Total Carbon Footprint
* Average Facility Emissions
* Emission Contribution by Load Type
* Carbon Intensity
* Emission Distribution

---

# Feature Engineering

The system automatically generates advanced sustainability features.

### Engineered Features

```text
Total_Power_Consumption

Reactive_Power_Ratio

Carbon_Intensity

Rolling_7_Day_Emission

Rolling_30_Day_Emission

Energy_Efficiency_Index

Peak_Load_Flag

Weekend_Flag

Seasonal_Usage_Index

Load_Type_Encoding
```

These features improve predictive performance and sustainability insights.

---

# Machine Learning Engine

## Objective

Predict future carbon emissions.

### Target Variable

```text
CO2(tCO2)
```

### Algorithms

1. Linear Regression
2. Random Forest Regressor
3. Gradient Boosting Regressor

### Automated Workflow

* Data Split
* Feature Scaling
* Cross Validation
* Hyperparameter Tuning
* Model Evaluation
* Best Model Selection

### Metrics

* R² Score
* RMSE
* MAE

### Model Output

```text
models/carbon_model.pkl
```

### Forecasting

The platform generates:

* Next-Day Emission Forecast
* Next-Week Emission Forecast
* Monthly Carbon Forecast

---

# Anomaly Detection Center

Isolation Forest is used for intelligent anomaly detection.

### Detects

* Energy Consumption Spikes
* CO₂ Emission Spikes
* Power Factor Deviations
* Reactive Power Abnormalities
* Load Pattern Anomalies

### Alert System

Each anomaly includes:

* Alert Level
* Severity Score
* Root Cause Indicator

Threshold Logic:

```text
1.5 × Rolling Median
```

---

# ESG Compliance Engine

The ESG module evaluates sustainability performance.

### Metrics

* Current Carbon Emissions
* Target Emissions
* Carbon Reduction %
* Sustainability Progress

### Traffic Light Status

🟢 Green → On Target

🟡 Yellow → Warning

🔴 Red → Exceeding Target

### Outputs

* ESG Compliance Score
* Sustainability Rating
* Carbon Reduction Recommendations

---

# Dashboard Modules

## Executive Summary

Executive-level KPIs:

* Total Emissions
* Average Daily Emissions
* Carbon Intensity
* ESG Score
* Active Alerts
* Energy Consumption

---

## Carbon Analytics

Visual carbon monitoring and emission breakdowns.

---

## Prediction Center

Machine learning forecasting dashboard.

---

## ESG Dashboard

Compliance tracking and sustainability scoring.

---

## Load Analysis

Industrial load behavior analysis.

---

## Anomaly Detection Center

Real-time anomaly monitoring.

---

## Sustainability Insights

AI-generated sustainability recommendations.

---

# Advanced Visualizations

The platform uses Plotly for interactive analytics.

### Included Charts

1. Carbon Emission Trend
2. Monthly Forecast
3. Energy Usage Trend
4. CO₂ Histogram
5. Carbon Intensity Trend
6. Load Type Comparison
7. ESG Gauge
8. Anomaly Scatter Plot
9. Energy Heatmap
10. Feature Importance
11. Weekly Emission Analysis
12. Sustainability Progress Dashboard

---

# AI Insights Engine

The platform automatically generates insights such as:

```text
Heavy Load contributed 42% of total emissions.

Carbon emissions increased 11% compared to previous month.

Peak consumption occurred on weekdays.

Reactive power inefficiency is increasing emissions.

ESG score improved by 8%.
```

### Recommendation Examples

* Optimize heavy-load operations.
* Improve power factor correction.
* Shift energy-intensive activities.
* Reduce peak-hour consumption.
* Upgrade energy-efficient equipment.

---

# MongoDB Atlas Integration

All results are persisted in MongoDB Atlas.

### Collections

```text
dataset_logs

emissions

predictions

alerts

esg_reports

insights
```

### Stored Data

* Uploaded Datasets
* Emission Reports
* Predictions
* ESG Reports
* Alerts
* AI Insights

---

# Project Structure

```text
project/

├── app.py
├── requirements.txt
├── README.md

├── data/

├── models/
│   └── carbon_model.pkl

├── pages/
│   ├── 1_Executive_Summary.py
│   ├── 2_Carbon_Analytics.py
│   ├── 3_Prediction_Center.py
│   ├── 4_ESG_Dashboard.py
│   ├── 5_Load_Analysis.py
│   ├── 6_Anomaly_Detection.py
│   └── 7_Sustainability_Insights.py

├── utils/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── emissions.py
│   ├── prediction.py
│   ├── anomaly_detection.py
│   ├── esg.py
│   ├── insights.py
│   ├── mongodb.py
│   └── visualizations.py

├── assets/

├── logs/

└── .env
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/yourusername/steel-esg-platform.git

cd steel-esg-platform
```

Create virtual environment.

```bash
python -m venv venv
```

Activate environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/

DATABASE_NAME=steel_esg_db
```

---

# Running the Application

Start Streamlit.

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

# MongoDB Atlas Setup

### Step 1

Create MongoDB Atlas account.

### Step 2

Create Cluster.

### Step 3

Create Database User.

### Step 4

Whitelist IP Address.

### Step 5

Copy Connection String.

### Step 6

Add Connection String to:

```env
MONGO_URI
```

---

# Deployment on Streamlit Cloud

### Push to GitHub

```bash
git init

git add .

git commit -m "Initial Commit"

git branch -M main

git remote add origin REPOSITORY_URL

git push -u origin main
```

---

### Streamlit Cloud

Open:

```text
https://share.streamlit.io
```

Choose:

```text
Repository

Branch

app.py
```

Add Secrets:

```toml
MONGO_URI="mongodb+srv://..."

DATABASE_NAME="steel_esg_db"
```

Deploy.

---

# Logging & Monitoring

Application logs are stored in:

```text
logs/app.log
```

Tracks:

* Upload Events
* Prediction Requests
* ESG Calculations
* Alerts
* Errors

---

# Security

Production recommendations:

* Store secrets in environment variables
* Enable MongoDB authentication
* Restrict Atlas network access
* Use HTTPS deployment
* Rotate credentials regularly

---

# Future Enhancements

### Advanced ML

* XGBoost
* LightGBM
* CatBoost

### Explainable AI

* SHAP
* LIME

### Reporting

* Automated ESG PDF Reports
* Executive Sustainability Reports

### Enterprise Features

* User Authentication
* Role-Based Access Control
* Real-Time Monitoring
* Scheduled Model Retraining

---

# Technology Stack

| Layer               | Technology      |
| ------------------- | --------------- |
| Frontend            | Streamlit       |
| Analytics           | Pandas          |
| Numerical Computing | NumPy           |
| Visualization       | Plotly          |
| Machine Learning    | Scikit-Learn    |
| Database            | MongoDB Atlas   |
| Model Storage       | Joblib          |
| Deployment          | Streamlit Cloud |
| Version Control     | GitHub          |

---

# License

MIT License

---

# Author

Steel Industry Carbon Footprint & ESG Analytics Platform

Built using Python, Machine Learning, ESG Analytics, MongoDB Atlas, Plotly, and Streamlit.
