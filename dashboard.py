
import pandas as pd
import streamlit as st
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objs as go
from datetime import datetime

# Set up the page configuration
st.set_page_config(page_title="HealthX", layout="wide")

# Load the datasets (adjust the file paths)
patients_df = pd.read_csv('/Users/tulasi/Desktop/HealthX/data/patients.csv')
encounters_df = pd.read_csv('/Users/tulasi/Desktop/HealthX/data/encounters.csv')
population_df = pd.read_csv('/Users/tulasi/Desktop/HealthX/data/Population(2010-2023).csv')
providers_df = pd.read_csv('/Users/tulasi/Desktop/HealthX/data/providers.csv')


# Preprocess data: Calculate AGE
patients_df['BIRTHDATE'] = pd.to_datetime(patients_df['BIRTHDATE'], errors='coerce')
current_date = pd.to_datetime('today')
patients_df['AGE'] = (current_date - patients_df['BIRTHDATE']).dt.days // 365

# Create Age Groups in 20-year intervals
age_groups = pd.cut(patients_df['AGE'], bins=[0, 20, 40, 60, 80, 100], labels=["0-20", "21-40", "41-60", "61-80", "81+"], right=False)

# Create a DataFrame with Age Group and the count of patients
age_groups_df = pd.DataFrame(age_groups.value_counts()).reset_index()
age_groups_df.columns = ['Age Group', 'Patient Count']

# Merge with encounter data to get the number of encounters per age group
encounters_age_group = pd.merge(encounters_df, patients_df[['Id', 'AGE']], left_on='PATIENT', right_on='Id', how='left')
encounters_age_group['Age Group'] = pd.cut(encounters_age_group['AGE'], bins=[0, 20, 40, 60, 80, 100], labels=["0-20", "21-40", "41-60", "61-80", "81+"], right=False)
encounter_count_by_age = encounters_age_group.groupby('Age Group').size().reset_index(name='Encounter Count')

# Merge age group statistics
age_stats_df = pd.merge(age_groups_df, encounter_count_by_age, on='Age Group')

# Calculate mean and median age
age_mean = patients_df['AGE'].mean()
age_median = patients_df['AGE'].median()

# Sidebar for page selection
st.sidebar.title("HealthX")  # Title only, no tagline
page = st.sidebar.radio("", ["Home", "Patient Demographics Analysis", "General Insights", "Predictive Insights", "About"])

# Main Page Content (Title and Tagline for Home)
if page == "Home":
    st.markdown(
        """
        <h1 style="font-size: 250px; text-align: center; font-weight: bold;">
            HealthX
        </h1>
        <p style="font-size: 28px; text-align: center;">
            Transforming complex healthcare data into actionable strategies to improve access, affordability, and availability for all communities.
        </p>
        """, unsafe_allow_html=True)

# Patient Demographics Analysis Page
elif page == "Patient Demographics Analysis":
    st.title("Patient Demographics Analysis")
    
    # Display sub-tabs for age distribution, gender analysis, etc., in a row using columns for buttons
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        age_distribution_button = st.button("Age Distribution")
    with col2:
        gender_analysis_button = st.button("Gender Analysis")
    with col3:
        geographic_distribution_button = st.button("Geographic Distribution")
    with col4:
        income_analysis_button = st.button("Income Analysis")
    
    if age_distribution_button:
        st.subheader("Age Distribution Analysis")
        # Display the KPI boxes for Mean and Median Age in the same row with some gap between them using st.columns
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div style="border: 2px solid #E6E6E6; padding: 20px; text-align: center;">
                    <h3>Mean Age</h3>
                    <p style="font-size: 36px; font-weight: bold;">{age_mean:.2f} years</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown(
                f"""
                <div style="border: 2px solid #E6E6E6; padding: 20px; text-align: center;">
                    <h3>Median Age</h3>
                    <p style="font-size: 36px; font-weight: bold;">{age_median:.2f} years</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Display the Age Group Distribution with encounter count inside a bordered box
        st.markdown(
            """
            <div style="border: 2px solid #E6E6E6; padding: 20px; margin-top: 20px;">
            """, unsafe_allow_html=True)
        
        age_group_dist_fig = px.bar(age_stats_df, x='Age Group', y='Patient Count', title="Age Group Distribution with Number of Patients")
        st.plotly_chart(age_group_dist_fig)

        st.markdown("</div>", unsafe_allow_html=True)

    elif gender_analysis_button:
        st.subheader("Gender Analysis")
        gender_dist = patients_df['GENDER'].value_counts().reset_index()
        gender_dist.columns = ['Gender', 'Count']
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div style="border: 2px solid #E6E6E6; padding: 20px; text-align: center;">
                    <h3>Male Patients</h3>
                    <p style="font-size: 36px; font-weight: bold;">{gender_dist[gender_dist['Gender'] == 'M']['Count'].values[0]}</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown(
                f"""
                <div style="border: 2px solid #E6E6E6; padding: 20px; text-align: center;">
                    <h3>Female Patients</h3>
                    <p style="font-size: 36px; font-weight: bold;">{gender_dist[gender_dist['Gender'] == 'F']['Count'].values[0]}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Gender Distribution Pie chart inside a bordered box
        st.markdown(
            """
            <div style="border: 2px solid #E6E6E6; padding: 20px; margin-top: 20px;">
            """, unsafe_allow_html=True)
        
        gender_pie_fig = px.pie(gender_dist, names='Gender', values='Count', title="Gender Distribution")
        st.plotly_chart(gender_pie_fig)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Males and Females by Age Group inside a bordered box
        st.markdown(
            """
            <div style="border: 2px solid #E6E6E6; padding: 20px; margin-top: 20px;">
            """, unsafe_allow_html=True)
        
        # Males and Females by Age Group
        gender_age_group_df = pd.merge(encounters_age_group, patients_df[['Id', 'GENDER']], left_on='PATIENT', right_on='Id', how='left')
        gender_age_group_counts = gender_age_group_df.groupby(['Age Group', 'GENDER']).size().reset_index(name='Encounter Count')
        
        # Plot bar chart for Gender and Age Group
        gender_age_group_fig = px.bar(gender_age_group_counts, x="Age Group", y="Encounter Count", color="GENDER", barmode='group', title="Encounters by Gender and Age Group")
        st.plotly_chart(gender_age_group_fig)

        st.markdown("</div>", unsafe_allow_html=True)

    elif geographic_distribution_button:
        st.subheader("Geographic Distribution")
    
        # Number of Patients in Different Races
        st.markdown("<h3>Number of Patients in Different Races</h3>", unsafe_allow_html=True)
        race_dist = patients_df['RACE'].value_counts().reset_index()
        race_dist.columns = ['Race', 'Count']
        st.write(race_dist)

        # Pie chart of percentage of different races
        st.markdown("<h3>Percentage of Different Races</h3>", unsafe_allow_html=True)
        race_pie_fig = px.pie(race_dist, names='Race', values='Count')
        st.plotly_chart(race_pie_fig)

        # Population of each city (2010-2023)
        st.markdown("<h3>Population of Each City (2010-2023)</h3>", unsafe_allow_html=True)
        st.write(population_df)
        
        # Top 10 cities with more encounters
        st.markdown("<h3>Top 10 Cities with More Encounters</h3>", unsafe_allow_html=True)

        # Merge encounters_df with the patients_df to get city information for each encounter
        encounters_with_city = pd.merge(encounters_df, patients_df[['Id', 'CITY']], left_on='PATIENT', right_on='Id', how='left')

        # Count encounters by city (using city from patients_df)
        encounters_by_city = encounters_with_city['CITY'].value_counts().reset_index()
        encounters_by_city.columns = ['City', 'Encounter Count']
        top_10_cities_encounters = encounters_by_city.head(10)
        encounters_fig = px.bar(top_10_cities_encounters, x='City', y='Encounter Count')
        st.plotly_chart(encounters_fig)

        
        # Income Analysis Page
    elif income_analysis_button:
        st.subheader("Income Analysis")

        # KPIs for Mean and Median Income
        mean_income = patients_df['INCOME'].mean()
        median_income = patients_df['INCOME'].median()

        # Display the KPI boxes for Mean and Median Income
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div style="border: 2px solid #E6E6E6; padding: 20px; text-align: center;">
                    <h3>Mean Income</h3>
                    <p style="font-size: 36px; font-weight: bold;">${mean_income:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown(
                f"""
                <div style="border: 2px solid #E6E6E6; padding: 20px; text-align: center;">
                    <h3>Median Income</h3>
                    <p style="font-size: 36px; font-weight: bold;">${median_income:,.2f}</p>
                </div>
                """, unsafe_allow_html=True)

        # Categorize income into income brackets (Bottom 20%, Lower-Middle 20%, etc.)
        income_labels = ['Bottom 20%', 'Lower-Middle 20%', 'Middle 20%', 'Upper-Middle 20%', 'Top 20%']
        income_bins = [0, patients_df['INCOME'].quantile(0.2), patients_df['INCOME'].quantile(0.4),
                    patients_df['INCOME'].quantile(0.6), patients_df['INCOME'].quantile(0.8), patients_df['INCOME'].max()]
        patients_df['Income Group'] = pd.cut(patients_df['INCOME'], bins=income_bins, labels=income_labels, right=False)

        # Income Distribution Pie chart
        income_dist = patients_df['Income Group'].value_counts().reset_index()
        income_dist.columns = ['Income Group', 'Count']
        income_pie_fig = px.pie(income_dist, names='Income Group', values='Count')
        st.plotly_chart(income_pie_fig)

        # Income Distribution Table
        st.markdown("<h3>Income Distribution by Group</h3>", unsafe_allow_html=True)
        st.write(income_dist)

        # Income Distribution by Race (Bar Chart)
        st.subheader("Income Distribution by Race")

        # Calculate the average income by race
        income_by_race = patients_df.groupby('RACE')['INCOME'].mean().reset_index()
        income_by_race.columns = ['Race', 'Average Income']

        # Bar chart for income distribution by race
        race_income_bar_fig = px.bar(income_by_race, x='Race', y='Average Income')
        st.plotly_chart(race_income_bar_fig)

        # Race with Income Percentages
        st.markdown("<h3>Income Distribution by Race</h3>", unsafe_allow_html=True)
        race_income_dist = patients_df.groupby('RACE')['INCOME'].mean().reset_index()
        race_income_dist.columns = ['Race', 'Average Income']
        st.write(race_income_dist)

        # Cities with the Least Income Level
        st.markdown("<h3>Cities with Least Average Income</h3>", unsafe_allow_html=True)
        city_income_dist = patients_df.groupby('CITY')['INCOME'].mean().reset_index()
        city_income_dist.columns = ['City', 'Average Income']
        city_income_dist_sorted = city_income_dist.sort_values('Average Income').head(10)
        st.write(city_income_dist_sorted)
    

# General Insights Page
elif page == "General Insights":
    st.title("📊 General Healthcare Overview")
    
    # Load executive data (use the correct path to your file)
    @st.cache_data
    def load_data():
        df = pd.read_csv('/Users/tulasi/Desktop/HealthX/data/executive summary data.csv', parse_dates=['START_x', 'STOP_x'])
        return df

    # Load population data (2010-2023)
    @st.cache_data
    def load_population_data():
        df = pd.read_csv('/Users/tulasi/Desktop/HealthX/data/population(2010-2023).csv')
        return df

    # Load data
    data = load_data()
    population_data = load_population_data()

    # City filter above KPIs, only for General Insights and Predictive Insights
    city_list = sorted(data['CITY_x'].unique())
    selected_city = st.selectbox("Select a City", city_list)  # Selecting the city here

    # Filter data for the selected city
    city_data = data[data['CITY_x'] == selected_city]
    population_city_data = population_data[population_data['CITY'] == selected_city]

    # Convert 'START_x' and 'START_y' to datetime, ignoring errors
    city_data['START_x'] = pd.to_datetime(city_data['START_x'], errors='coerce')
    city_data['START_y'] = pd.to_datetime(city_data['START_y'], errors='coerce')

    # Calculate the Diagnosis to Treatment time in hours
    city_data['DIAGNOSIS_TO_TREATMENT'] = (city_data['START_y'] - city_data['START_x']).dt.total_seconds() / 3600

    # KPI Layout (using st.columns for separate boxes)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_encounters = len(city_data)
        st.metric("Total Encounters", total_encounters)
    
    with col2:
        avg_coverage = city_data['PAYER_COVERAGE_x'].mean()
        st.metric("Average Healthcare Coverage", f"{avg_coverage:.2f}")
    
    with col3:
        adherence_rate = city_data['DISPENSES'].sum() / city_data['ENCOUNTERS'].sum() if city_data['ENCOUNTERS'].sum() > 0 else 0
        st.metric("Adherence Rate", f"{adherence_rate:.2f}")
    
    with col4:
        avg_diagnosis_to_treatment_time = city_data['DIAGNOSIS_TO_TREATMENT'].mean()
        st.metric("Avg Diagnosis to Treatment Time", f"{avg_diagnosis_to_treatment_time:.2f} hours")

    # Graph Layout
    # Graph 1: Encounters Over Years (Line)
    encounters_over_years = city_data.groupby(city_data['START_x'].dt.year)['Id_x'].count().reset_index(name='NUM_ENCOUNTERS')
    encounters_fig = px.line(encounters_over_years, x='START_x', y='NUM_ENCOUNTERS', title="Encounters Over Years")
    st.plotly_chart(encounters_fig, key="encounters_fig", use_container_width=True)

    # Graph 2: Provider to Patient Ratio Over Years (Line)
    provider_patient_ratio = city_data.groupby(city_data['START_x'].dt.year).agg({'PROVIDER': 'nunique', 'PATIENT': 'nunique'}).reset_index()
    provider_patient_ratio['RATIO'] = provider_patient_ratio['PROVIDER'] / provider_patient_ratio['PATIENT']
    ratio_fig = px.line(provider_patient_ratio, x='START_x', y='RATIO', title="Provider to Patient Ratio Over Years")
    st.plotly_chart(ratio_fig, key="ratio_fig", use_container_width=True)

    # Graph 3: Healthcare Expenses by Category (Pie Chart)
    expenses_by_category = city_data['ENCOUNTERCLASS'].value_counts().reset_index(name='COUNT')
    expenses_by_category.columns = ['Category', 'Count']
    expenses_pie = px.pie(expenses_by_category, names='Category', values='Count', title="Healthcare Expenses by Category")
    st.plotly_chart(expenses_pie, key="expenses_pie", use_container_width=True)

    # Graph 4: Claim Cost Over Years (Bar Graph)
    claim_cost_over_years = city_data.groupby(city_data['START_x'].dt.year)['TOTAL_CLAIM_COST'].sum().reset_index(name='TOTAL_CLAIM_COST')
    claim_cost_fig = px.bar(claim_cost_over_years, x='START_x', y='TOTAL_CLAIM_COST', title="Claim Cost Over Years")
    st.plotly_chart(claim_cost_fig, key="claim_cost_fig", use_container_width=True)

    # Graph 5: Medication Distribution by Type (Pie Chart)
    medication_distribution = city_data['CATEGORY'].value_counts().reset_index(name='COUNT')
    medication_distribution.columns = ['Medication', 'Count']
    medication_pie = px.pie(medication_distribution, names='Medication', values='Count', title="Medication Distribution by Type")
    st.plotly_chart(medication_pie, key="medication_pie", use_container_width=True)

    # Graph 6: Healthcare Expenses Forecasting (Line)
    expenses_data = city_data.groupby(city_data['START_x'].dt.year)['HEALTHCARE_EXPENSES'].sum()
    expenses_fig = px.line(expenses_data, x=expenses_data.index, y=expenses_data.values, title="Healthcare Expenses Over Years")
    st.plotly_chart(expenses_fig, key="expenses_fig", use_container_width=True)


# Predictive Insights Page
elif page == "Predictive Insights":
    st.header("📈 Predictive Analytics")
    st.write("""
        This section will show forecast trends for healthcare metrics, including population, claim costs, encounters, and providers.
    """)
    
    # Load executive data (use the correct path to your file)
    @st.cache_data
    def load_data():
        df = pd.read_csv('/Users/tulasi/Desktop/HealthX/data/executive summary data.csv', parse_dates=['START_x', 'STOP_x'])
        return df

    # Load population data (2010-2023)
    @st.cache_data
    def load_population_data():
        df = pd.read_csv('/Users/tulasi/Desktop/HealthX/data/population(2010-2023).csv')
        return df

    # Load data
    data = load_data()
    population_data = load_population_data()

    # City filter above KPIs, only for General Insights and Predictive Insights
    city_list = sorted(data['CITY_x'].unique())
    selected_city = st.selectbox("Select a City", city_list)  # Selecting the city here

    # Filter data for the selected city
    city_data = data[data['CITY_x'] == selected_city]
    population_city_data = population_data[population_data['CITY'] == selected_city]

    # Convert 'START_x' and 'START_y' to datetime, ignoring errors
    city_data['START_x'] = pd.to_datetime(city_data['START_x'], errors='coerce')
    city_data['START_y'] = pd.to_datetime(city_data['START_y'], errors='coerce')

    # Calculate the Diagnosis to Treatment time in hours
    city_data['DIAGNOSIS_TO_TREATMENT'] = (city_data['START_y'] - city_data['START_x']).dt.total_seconds() / 3600


    # **Forecasting Functions**
    # Here we are using ARIMA to forecast the next 5 years for Population, Claim Cost, Encounters, and Providers

    # Function to forecast population
    def forecast_population(city, forecast_steps=5):  # Predicting from 2025 to 2029
        city_population_data = population_city_data.drop(columns=['CITY'])
        city_population_data = city_population_data.T  # Transpose to get years as index
        city_population_data.columns = [selected_city]  # Set city name as the column label
        
        time_series_data = city_population_data[selected_city]
        model = ARIMA(time_series_data, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_steps)
        forecast_years = list(range(2025, 2025 + forecast_steps))

        trace1 = go.Scatter(
            x=time_series_data.index,
            y=time_series_data,
            mode='lines',  # Solid line for actual data
            name='Actual Population',
            line=dict(color='white')  # White solid line for actual data
        )

        trace2 = go.Scatter(
            x=forecast_years,
            y=forecast,
            mode='markers+lines',
            name='Forecasted Population',
            marker=dict(color='red', symbol='circle'),
            line=dict(dash='solid')  # Solid red line for forecasted data
        )

        figure = {
            'data': [trace1, trace2],
            'layout': go.Layout(
                title=f'{selected_city} - Population Forecast (2025–2029)',
                xaxis={'title': 'Year', 'tickvals': list(range(2010, 2030)), 'tickangle': 45},
                yaxis={'title': 'Population'},
                hovermode='closest'
            )
        }
        return figure

    # Forecast Population and Show Plot
    population_fig = forecast_population(selected_city)
    st.plotly_chart(population_fig, key="population_fig", use_container_width=True)

    # Claim Cost Forecasting (Line)
    def forecast_claim_cost(city, forecast_steps=5):  # Predicting from 2025 to 2029
        claim_cost_data = city_data.groupby(city_data['START_x'].dt.year)['TOTAL_CLAIM_COST'].sum()
        model = ARIMA(claim_cost_data, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_steps)
        forecast_years = list(range(2025, 2025 + forecast_steps))

        trace1 = go.Scatter(
            x=claim_cost_data.index,
            y=claim_cost_data.values,
            mode='lines',  # Solid line for actual data
            name='Actual Claim Costs',
            line=dict(color='white')
        )

        trace2 = go.Scatter(
            x=forecast_years,
            y=forecast,
            mode='markers+lines',
            name='Forecasted Claim Costs',
            marker=dict(color='red', symbol='circle'),
            line=dict(dash='solid')  # Solid red line for forecasted data
        )

        figure = {
            'data': [trace1, trace2],
            'layout': go.Layout(
                title=f'{selected_city} - Claim Cost Forecast (2025–2029)',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Claim Costs'},
                hovermode='closest'
            )
        }
        return figure

    # Forecast Claim Cost and Show Plot
    claim_cost_fig = forecast_claim_cost(selected_city)
    st.plotly_chart(claim_cost_fig, key="claim_cost_fig", use_container_width=True)

    # Encounters Forecasting (Line)
    def forecast_encounters(city, forecast_steps=5):  # Predicting from 2025 to 2029
        encounters_data = city_data.groupby(city_data['START_x'].dt.year)['Id_x'].count()
        model = ARIMA(encounters_data, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_steps)
        forecast_years = list(range(2025, 2025 + forecast_steps))

        trace1 = go.Scatter(
            x=encounters_data.index,
            y=encounters_data.values,
            mode='lines',  # Solid line for actual data
            name='Actual Encounters',
            line=dict(color='white')  # White solid line for actual data
        )

        trace2 = go.Scatter(
            x=forecast_years,
            y=forecast,
            mode='markers+lines',
            name='Forecasted Encounters',
            marker=dict(color='red', symbol='circle'),
            line=dict(dash='solid')  # Solid red line for forecasted data
        )

        figure = {
            'data': [trace1, trace2],
            'layout': go.Layout(
                title=f'{selected_city} - Encounters Forecast (2025–2029)',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Encounters'},
                hovermode='closest'
            )
        }
        return figure

    # Forecast Encounters and Show Plot
    encounters_fig = forecast_encounters(selected_city)
    st.plotly_chart(encounters_fig, key="encounters_fig", use_container_width=True)

    # Providers Forecasting (Line)
    def forecast_providers(city, forecast_steps=5):  # Predicting from 2025 to 2029
        providers_data = city_data.groupby(city_data['START_x'].dt.year)['PROVIDER'].nunique()
        model = ARIMA(providers_data, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_steps)
        forecast_years = list(range(2025, 2025 + forecast_steps))

        trace1 = go.Scatter(
            x=providers_data.index,
            y=providers_data.values,
            mode='lines',  # Solid line for actual data
            name='Actual Providers',
            line=dict(color='white')  # White solid line for actual data
        )

        trace2 = go.Scatter(
            x=forecast_years,
            y=forecast,
            mode='markers+lines',
            name='Forecasted Providers',
            marker=dict(color='red', symbol='circle'),
            line=dict(dash='solid')  # Solid red line for forecasted data
        )

        figure = {
            'data': [trace1, trace2],
            'layout': go.Layout(
                title=f'{selected_city} - Providers Forecast (2025–2029)',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Providers'},
                hovermode='closest'
            )
        }
        return figure

    # Forecast Providers and Show Plot
    providers_fig = forecast_providers(selected_city)
    st.plotly_chart(providers_fig, key="providers_fig", use_container_width=True)

    # New Graph: Healthcare Expenses Forecasting (Line)
    def forecast_expenses(city, forecast_steps=5):  # Predicting from 2025 to 2029
        expenses_data = city_data.groupby(city_data['START_x'].dt.year)['HEALTHCARE_EXPENSES'].sum()
        model = ARIMA(expenses_data, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=forecast_steps)
        forecast_years = list(range(2025, 2025 + forecast_steps))

        trace1 = go.Scatter(
            x=expenses_data.index,
            y=expenses_data.values,
            mode='lines',  # Solid line for actual data
            name='Actual Healthcare Expenses',
            line=dict(color='white')
        )

        trace2 = go.Scatter(
            x=forecast_years,
            y=forecast,
            mode='markers+lines',
            name='Forecasted Expenses',
            marker=dict(color='red', symbol='circle'),
            line=dict(dash='solid')  # Solid red line for forecasted data
        )

        figure = {
            'data': [trace1, trace2],
            'layout': go.Layout(
                title=f'{selected_city} - Healthcare Expenses Forecast (2025–2029)',
                xaxis={'title': 'Year'},
                yaxis={'title': 'Healthcare Expenses'},
                hovermode='closest'
            )
        }
        return figure

    # Forecast Expenses and Show Plot
    expenses_fig = forecast_expenses(selected_city)
    st.plotly_chart(expenses_fig, key="expenses_fig", use_container_width=True)

elif page == "About":
    st.header("ℹ️ About This Project")
    st.write("""
        This section will explain the purpose, data, and team behind HealthX.
    """)
    
    st.subheader("About the Project")
    st.write("""
        HealthX is a data-powered healthcare analytics platform dedicated to uncovering and addressing disparities in healthcare access across diverse communities. 
        Built on the principles of the 5 A’s of Healthcare—Accessibility, Affordability, Availability, Accommodation, and Acceptability—HealthX transforms complex datasets 
        into actionable insights using advanced analytics and predictive modeling.
        
        By leveraging AI and machine learning, HealthX forecasts key healthcare trends such as encounter rates, provider availability, and chronic disease patterns to help public health administrators, 
        policymakers, and stakeholders make informed, equitable decisions.
        
        Our mission is simple but powerful:
        To bridge the gap in healthcare access by turning real-time data into smarter solutions for a healthier, more inclusive future.
    """)

    st.subheader("About the Data")
    st.write("""
        The data used in **HealthX** includes a combination of **synthetic health data** from **Synthea-generated health records** and **US Census population data**. 
        These datasets allow us to generate real-time insights and predictive analytics that address healthcare disparities. Below is a breakdown of the key data used in the project:
        
        1. **Synthea-Generated Health Data**:
            - **Conditions**: Contains information about the medical conditions diagnosed in patients. This dataset helps identify the most prevalent health issues in different regions and demographic groups, assisting in understanding healthcare needs and utilization patterns.
            - **Claims**: Provides data on healthcare costs, total claim amounts, insurance coverage, and reimbursements. This dataset is vital for analyzing healthcare affordability, the financial burden on patients, and understanding claim patterns across various healthcare services.
            - **Encounters**: Tracks healthcare visits, procedures, and treatments. It provides insights into healthcare access and utilization, including the frequency of medical interactions and the types of services provided.
            - **Medication**: Includes data on medication refills, dispensations, and adherence rates. This dataset is used to track patient compliance with prescribed medications and evaluate the effectiveness of treatment regimens.
            - **Patient**: Contains demographic information about patients, such as age, gender, race, income, and other personal details. This data is crucial for understanding disparities in healthcare access across different population groups.
        
        2. **US Census Population Data (2010-2023)**:
            This dataset provides population data, which is crucial for understanding demographic shifts and regional disparities in healthcare access. The **US Census population data** is used in HealthX for forecasting population trends in various cities, allowing us to project future healthcare needs.
        
        3. **Provider**: Includes information on healthcare providers, such as availability, specialties, and patient-to-provider ratios. This dataset helps assess the distribution and accessibility of healthcare services in different regions, aiding in the analysis of healthcare supply and demand.
    """)

    st.subheader("About Synthea")
    st.write("""
        Synthea is an open-source project that generates synthetic healthcare data for modeling and testing purposes. It produces comprehensive, realistic datasets for 
        health systems, including demographic data, health encounters, conditions, medications, and treatments. HealthX uses these datasets to simulate real-world healthcare scenarios, 
        ensuring that our insights are grounded in data-driven predictions.
    """)

    st.subheader("Team Members")
    st.write("""
        - Udaya Lakshmi Boddu
        - Meer Anas Ali
        - Naga Tulasi Velamakanni
        - Harsha Vardhan Nallamothu
        - Renusri Darukumalli
    """)
