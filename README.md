# HealthX: Healthcare Access & Equity Dashboard
HealthX is an innovative Streamlit-powered web application developed as part of a Master’s Research Project to help public health administrators, policy analysts, and healthcare providers evaluate and address healthcare disparities. HealthX delivers real-time, actionable insights into healthcare accessibility, affordability, and availability across different cities and demographic groups, supporting data-driven strategies for improving health equity.

# Key Features
**Healthcare Access Overview:** Provides interactive dashboards analyzing patient encounters, provider availability, and claim distributions by city, age group, gender, and race to highlight disparities in healthcare delivery.

**Predictive Analysis & Forecasting:** Integrates time-series forecasting models (e.g., Prophet, ARIMA) and machine learning techniques to project future trends in healthcare access, demand, and disparities over the next 5-10 years.

**Population Demographics Explorer:** Presents detailed demographic insights (age, gender, race, income, geography) with interactive filters for city-wise and group-wise exploration.

**Cost & Payer Analysis:** Displays trends in healthcare costs, insurance coverage, and claim transactions to identify financial barriers to access.

**Dynamic Visualizations:** Offers an array of charts including heatmaps, bar charts, line graphs, scatter plots, KPIs, and maps using Plotly, Matplotlib, and Altair — designed for both high-level summaries and deep-dive analytics.

**User-Friendly Interface:** Features a clean, modular Streamlit web app with dedicated pages:

  General Access Insights
  
  Predictive Analysis
  
  Demographics Explorer
  
  Cost & Claims Analysis

# About HealthX

**Programming Language:** Python

**Web Framework:** Streamlit

**Data Manipulation: **Pandas, NumPy

**Visualization:** Plotly, Matplotlib, Altair

**Machine Learning:** Scikit-learn (Logistic Regression, Random Forest)

**Time Series Forecasting:** Prophet, Statsmodels (ARIMA)

**Database Interaction (Conceptual):** PostgreSQL / Supabase

**BI Tool (Conceptual): **Tableau

# Installation
**Clone the repository:**

bash
Copy
git clone https://github.com/yourusername/healthx-dashboard.git  
cd healthx-dashboard  

**Create a virtual environment:**

bash
Copy
python -m venv venv  
source venv/bin/activate  # On Linux / Mac  
venv\Scripts\activate     # On Windows  

**Install dependencies:**

bash
Copy
pip install -r requirements.txt  

**Run the dashboard:**

bash
Copy
streamlit run app.py 

# Data Requirements

The system is designed to operate on structured healthcare datasets (CSV format) generated from sources like Synthea. Required datasets include:

  patients.csv → Demographic data
  
  encounters.csv → Records of patient visits
  
  providers.csv → Provider and facility data
  
  conditions.csv → Chronic and acute condition records
  
  claims.csv, claims_transactions.csv → Insurance claims and payments
  
  payer_transitions.csv → Insurance coverage changes
  
  observations.csv, medications.csv → Vital signs, prescriptions

