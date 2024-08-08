import streamlit as st
import requests
import plotly.express as px
from streamlit_option_menu import option_menu

# Streamlit application setup
st.set_page_config(layout="wide")
st.title("Battery Data Dashboard")

# Function to fetch data from the Flask API
def fetch_data(endpoint):
    response = requests.get(f'http://localhost:8080/{endpoint}')
    if response.status_code != 200:
        st.error(f"Failed to fetch data from {endpoint}")
        return None
    return response.json()

# Sidebar navigation panel
with st.sidebar:
    selected_option = option_menu(
        "Navigation",
        ["Dashboard", "Cell ID 5308", "Cell ID 5329"],
        icons=["speedometer", "battery-half", "battery-half"],
        menu_icon="cast",
        default_index=0,
    )

def display_soh_report(cell_ids):
    col1, col2 = st.columns(2)
    for i, cell_id in enumerate(cell_ids):
        soh_data = fetch_data(f'soh/{cell_id}')
        if not soh_data:
            continue
        with col1 if i == 0 else col2:
            st.write(f"State of Health (SoH) for Cell {cell_id}")
            fig = px.pie(values=[soh_data['soh'], 100-soh_data['soh']], names=['SoH', 'Remaining'])
            st.plotly_chart(fig)

def display_cell_data(cell_id):
    # Display insights
    st.write(f"Insights for Cell {cell_id}")
    st.write("The following charts provide a detailed view of the cell's performance metrics over time.")
    
    # Voltage vs. Time chart
    voltage_data = fetch_data(f'voltage/{cell_id}')
    fig = px.line(voltage_data, x='time', y='voltage', title='Voltage vs. Time')
    st.plotly_chart(fig)

    # Current vs. Time chart
    current_data = fetch_data(f'current/{cell_id}')
    fig = px.line(current_data, x='time', y='current', title='Current vs. Time')
    st.plotly_chart(fig)

    # Temperature vs. Time chart
    temperature_data = fetch_data(f'temperature/{cell_id}')
    fig = px.line(temperature_data, x='time', y='temperature', title='Temperature vs. Time')
    st.plotly_chart(fig)

    # Capacity vs. Time chart
    capacity_data = fetch_data(f'capacity/{cell_id}')
    fig = px.line(capacity_data, x='time', y='capacity', title='Capacity vs. Time')
    st.plotly_chart(fig)

cell_ids = fetch_data('cells')
if not cell_ids:
    st.error("No cell IDs found. Ensure the database is populated and the Flask server is running.")
else:
    if selected_option == "Dashboard":
        st.header("State of Health Report")
        display_soh_report(cell_ids[:2])  # Assuming you want to display SoH for the first two cells side by side
    elif selected_option == "Cell ID 5308":
        st.header("Cell ID 5308")
        display_cell_data(5308)
    elif selected_option == "Cell ID 5329":
        st.header("Cell ID 5329")
        display_cell_data(5329)
