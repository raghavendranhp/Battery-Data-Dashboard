import streamlit as st
import requests
import plotly.express as px
from streamlit_option_menu import option_menu

#Ignore FutureWarnings to avoid clutter in the output
import warnings 
warnings.filterwarnings("ignore", category=FutureWarning)
from pathlib import Path

# Get the absolute path to the directory containing the current script
path = Path(__file__).parent.resolve()

# Add the path to sys.path if needed
import sys
sys.path.append(str(path))

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
    # State of Health values
    soh_values = {
        5308:  round((2992.02 / 3000) * 100, 2),
        5329:  round((2822.56 / 3000) * 100, 2)
    }
    
    if len(cell_ids) < 2:
        st.error("Not enough cell IDs to display SoH reports.")
        return

    # Fixed layout for SoH charts
    col1, col2 = st.columns(2)

    for i, cell_id in enumerate(cell_ids[:2]):
        soh = soh_values.get(cell_id, None)
        if soh is None:
            st.error(f"State of Health data not available for Cell {cell_id}.")
            continue

        with (col1 if i == 0 else col2):
            
            fig = px.pie(values=[soh, 100-soh], names=['SoH', 'Remaining'], 
                         title=f"State of Health for Cell {cell_id}")
            st.plotly_chart(fig, use_container_width=True)
def display_dashboard():
    st.header("Dashboard Overview")
    st.markdown("""
    Welcome to the Battery Data Dashboard!

    This project aims to provide an insightful analysis of battery cell performance. By visualizing key metrics, this dashboard helps in understanding the health and performance trends of different battery cells.

    ## State of Health (SoH)
    The State of Health (SoH) is a critical metric that indicates the overall condition of a battery cell. It is calculated based on the ratio of the cell's discharge capacity to its nominal capacity, expressed as a percentage. Higher SoH values represent better battery health.

    ## Project Overview
    This dashboard provides various performance metrics for battery cells, including:
    
    - **State of Health (SoH)**: A pie chart representing the health of each cell.
    - **Voltage, Current, Temperature, and Capacity Over Time**: Detailed line charts that show how these metrics vary over time for individual cells.

    The insights derived from these visualizations assist in assessing battery performance, planning maintenance, and improving overall battery management strategies.

    ## Creator Details
    - **Name**: Raghavendran S.
    - **Contact**: raghavendranhp@gmail.com
    - **Location**: Erode, Tamil Nadu

    Feel free to explore the charts to gain a deeper understanding of the battery cells' performance. Use the navigation panel to switch between different views and analyze specific cell data.
    """)

def display_soh_report_data(cell_ids):#using data from dataset
    # Ensure there are at least two cell IDs
    if len(cell_ids) < 2:
        st.error("Not enough cell IDs to display SoH reports.")
        return

    # Fixed layout for SoH charts
    col1, col2 = st.columns(2)

    for i, cell_id in enumerate(cell_ids[:2]):
        soh_data = fetch_data(f'soh/{cell_id}')
        if not soh_data:
            continue

        with (col1 if i == 0 else col2):
            st.write(f"State of Health (SoH) for Cell {cell_id}")
            fig = px.pie(values=[soh_data['soh'], 100-soh_data['soh']], names=['SoH', 'Remaining'])
            st.plotly_chart(fig, use_container_width=True)


def display_cell_data(cell_id):
    # Fetch data for all charts
    voltage_data = fetch_data(f'voltage/{cell_id}')
    current_data = fetch_data(f'current/{cell_id}')
    temperature_data = fetch_data(f'temperature/{cell_id}')
    capacity_data = fetch_data(f'capacity/{cell_id}')

    if not (voltage_data and current_data and temperature_data and capacity_data):
        st.error("Failed to fetch all required data.")
        return

    
    # Fixed layout for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Voltage vs. Time chart
        fig1 = px.line(voltage_data, x='time', y='voltage', title='Voltage vs. Time')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        # Current vs. Time chart
        fig2 = px.line(current_data, x='time', y='current', title='Current vs. Time')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Adding space between top and bottom sections
    st.markdown("<br>", unsafe_allow_html=True)

    # Fixed layout for bottom charts
    col3, col4 = st.columns(2)
    
    with col3:
        # Temperature vs. Time chart
        fig3 = px.line(temperature_data, x='time', y='temperature', title='Temperature vs. Time')
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        # Capacity vs. Time chart
        fig4 = px.line(capacity_data, x='time', y='capacity', title='Capacity vs. Time')
        st.plotly_chart(fig4, use_container_width=True)
    # Display insights
    st.info(f"## Insights for Cell {cell_id}")
    st.info(f"We understand while charging Temperature of cell {cell_id} gets incresed.")
    

cell_ids = fetch_data('cells')
if not cell_ids:
    st.error("No cell IDs found. Ensure the database is populated and the Flask server is running.")
else:
    if selected_option == "Dashboard":
        st.header("State of Health Report")
        display_soh_report(cell_ids[:2]) 
        display_dashboard() 
    elif selected_option == "Cell ID 5308":
        st.header("Cell ID 5308")
        display_cell_data(5308)
    elif selected_option == "Cell ID 5329":
        st.header("Cell ID 5329")
        display_cell_data(5329)
