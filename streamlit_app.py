import streamlit as st
import requests
import plotly.express as px

# Streamlit application setup
st.title("Battery Data Dashboard")

# Function to fetch data from the Flask API
def fetch_data(endpoint):
    response = requests.get(f'http://localhost:8080/{endpoint}')
    st.error(f'Request URL: http://localhost:8080/{endpoint}')
    st.error(f'Status Code: {response.status_code}')
    #print(f'Response Text: {response.text}')
    return response.json()

# Select cell ID
cell_ids = fetch_data('cells')
if not cell_ids:
    st.error("No cell IDs found. Ensure the database is populated and the Flask server is running.")
else:
    selected_cell_id = st.selectbox('Select Cell ID', cell_ids)

    # State of Health (SoH) pie chart
    soh_data = fetch_data(f'soh/{selected_cell_id}')
    st.write("State of Health (SoH)")
    fig = px.pie(values=[soh_data['soh'], 100-soh_data['soh']], names=['SoH', 'Remaining'])
    st.plotly_chart(fig)

    # Voltage vs. Time chart
    voltage_data = fetch_data(f'voltage/{selected_cell_id}')
    fig = px.line(voltage_data, x='time', y='voltage', title='Voltage vs. Time')
    st.plotly_chart(fig)

    # Current vs. Time chart
    current_data = fetch_data(f'current/{selected_cell_id}')
    fig = px.line(current_data, x='time', y='current', title='Current vs. Time')
    st.plotly_chart(fig)

    # Temperature vs. Time chart
    temperature_data = fetch_data(f'temperature/{selected_cell_id}')
    fig = px.line(temperature_data, x='time', y='temperature', title='Temperature vs. Time')
    st.plotly_chart(fig)

    # Capacity vs. Time chart
    capacity_data = fetch_data(f'capacity/{selected_cell_id}')
    fig = px.line(capacity_data, x='time', y='capacity', title='Capacity vs. Time')
    st.plotly_chart(fig)
