# 🏭 Steel Industry Carbon Footprint & ESG Analytics Platform

## AI-Powered Carbon Forecasting, ESG Intelligence & Digital Twin System

### Overview

The Steel Industry Carbon Footprint & ESG Analytics Platform is an enterprise-grade sustainability intelligence solution designed for steel manufacturing facilities.

The platform combines:

* Carbon Emission Analytics
* ESG Compliance Monitoring
* Machine Learning Forecasting
* Time Series Forecasting
* AutoML Model Selection
* Monte Carlo Risk Simulation
* Facility Digital Twin
* Future Scenario Simulation
* MongoDB Atlas Data Management
* Interactive Streamlit Dashboards

The system enables organizations to analyze historical emissions, forecast future carbon footprints, evaluate ESG performance, simulate operational changes, and optimize sustainability strategies.

---

# Key Features

## Carbon Footprint Analytics

* Daily Emission Analysis
* Weekly Emission Analysis
* Monthly Emission Analysis
* Annualized Carbon Footprint
* Carbon Intensity Monitoring
* Emission Distribution Analysis
* Load-Type Contribution Analysis

---

## ESG Compliance Engine

* ESG Compliance Score
* Sustainability Rating
* Carbon Reduction Tracking
* ESG Progress Monitoring
* Traffic-Light Compliance Status

### Compliance Levels

| Status | Description      |
| ------ | ---------------- |
| Green  | On Target        |
| Yellow | Warning          |
| Red    | Exceeding Target |

---

## Machine Learning Prediction Center

Supported Models:

* Linear Regression
* Ridge Regression
* Lasso Regression
* ElasticNet
* Random Forest Regressor
* Extra Trees Regressor
* Gradient Boosting Regressor
* AdaBoost Regressor
* HistGradientBoosting Regressor
* XGBoost Regressor
* LightGBM Regressor
* CatBoost Regressor

Performance Metrics:

* R² Score
* RMSE
* MAE
* MAPE
* Cross Validation Score

---

## AutoML Engine

The platform automatically:

* Trains all supported models
* Performs Cross Validation
* Runs Hyperparameter Optimization
* Calculates Weighted Scores
* Selects the Best Model
* Saves Production Models

Model Storage:

```text
models/
├── carbon_model.pkl
└── best_carbon_model.pkl
```

Weighted Ranking Formula:

40% R²

30% RMSE

20% MAE

10% Stability Score

---

## Future Scenario Lab

Digital Twin powered simulation environment.

Users can modify:

* Energy Usage
* Power Factor
* Reactive Power
* Production Growth
* Load Mix
* Renewable Energy Adoption
* Carbon Reduction Initiatives
* Energy Optimization Programs
* Predictive Maintenance Plans

Instantly Predict:

* Future CO₂ Emissions
* Future Energy Consumption
* Future ESG Score
* Future Carbon Intensity
* Future Sustainability Rating
* Future Anomaly Risk

---

## Time Series Forecasting

Supported Forecasting Models:

* Prophet
* SARIMA
* Exponential Smoothing
* Random Forest Time Series
* XGBoost Time Series
* LightGBM Time Series

Forecast Horizons:

* 30 Days
* 90 Days
* 180 Days
* 365 Days

Forecast Outputs:

* Future Emissions
* ESG Trends
* Carbon Intensity Trends
* Sustainability Score Forecasts

---

## Monte Carlo Simulation

Risk Analysis Engine

Simulation Runs:

1000 Iterations

Outputs:

* Best Case Scenario
* Average Case Scenario
* Worst Case Scenario
* Emission Probability Distribution
* Carbon Budget Consumption
* Risk Score

---

## Anomaly Detection Center

Powered by Isolation Forest

Detects:

* Usage Spikes
* Emission Spikes
* Reactive Power Anomalies
* Power Factor Deviations
* Load Pattern Abnormalities

Generates:

* Alert Levels
* Severity Scores
* Root Cause Indicators

---

# Dashboard Pages

```text
pages/

1_Executive_Summary.py
2_Carbon_Analytics.py
3_Prediction_Center.py
4_ESG_Dashboard.py
5_Load_Analysis.py
6_Anomaly_Detection.py
7_Sustainability_Insights.py
8_Future_Scenario_Lab.py
9_Model_Comparison.py
```

---

# Project Structure

```text
project/

├── app.py
├── requirements.txt
├── README.md

├── config/

├── data/

├── models/

├── pages/

├── utils/

├── assets/

└── logs/
```

---

# Dataset

Expected Dataset:

```text
Steel_industry_data.csv
```

Columns:

```text
Usage_kWh
Lagging_Current_Reactive.Power_kVarh
Leading_Current_Reactive_Power_kVarh
CO2(tCO2)
Lagging_Current_Power_Factor
Leading_Current_Power_Factor
NSM
WeekStatus
Day_of_week
Load_Type
Date
```

---

# MongoDB Atlas Integration

Collections:

```text
dataset_logs

emissions

predictions

alerts

esg_reports

insights

future_scenarios

forecasts

model_scores

simulation_results

digital_twin
```

---

# Installation

Clone Repository

```bash
git clone https://github.com/yourusername/steel-esg-platform.git

cd steel-esg-platform
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
MONGO_URI=your_mongodb_connection_string

DB_NAME=steel_esg

MODEL_PATH=models/best_carbon_model.pkl

LOG_LEVEL=INFO
```

---

# Run Locally

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

# Streamlit Cloud Deployment

Push Project to GitHub

Connect Repository to Streamlit Cloud

Deploy using:

```text
app.py
```

Add Secrets:

```toml
MONGO_URI="your_connection_string"
DB_NAME="steel_esg"
```

---

# Production Features

* Streamlit Caching
* Session State Management
* MongoDB Persistence
* Joblib Model Storage
* Logging & Monitoring
* Error Handling
* AutoML Pipelines
* GridSearchCV
* RandomizedSearchCV
* Forecast Confidence Intervals
* Digital Twin Simulations

---

# Visualizations

Implemented Using Plotly

* Carbon Trend Analysis
* Forecast Confidence Bands
* Monte Carlo Fan Charts
* ESG Gauge Charts
* Carbon Budget Tracker
* Feature Importance Analysis
* Model Leaderboard
* Sustainability Dashboard
* Forecast Heatmaps
* Scenario Comparison Charts

---

# Business Benefits

The platform enables organizations to:

* Reduce Carbon Emissions
* Improve ESG Compliance
* Optimize Energy Usage
* Forecast Future Sustainability Performance
* Evaluate Operational Scenarios
* Identify Emission Risks
* Support Executive Decision Making

---

# Technology Stack

Frontend

* Streamlit

Data Analytics

* Pandas
* NumPy

Machine Learning

* Scikit-Learn
* XGBoost
* LightGBM
* CatBoost

Forecasting

* Prophet
* SARIMA
* Exponential Smoothing

Visualization

* Plotly

Database

* MongoDB Atlas

Deployment

* Streamlit Cloud
* Docker
* AWS
* Azure
* Render

---

# License

MIT License

---

# Author

Steel Industry Carbon Footprint & ESG Analytics Platform

Enterprise Sustainability Intelligence Suite

Version 2.0
