# 



# Battery Data Dashboard

## Overview

This project is a simple three-page dashboard for visualizing the performance of Li-ion cells. The dashboard displays various metrics such as State of Health (SoH), Voltage, Current, Temperature, and Capacity over time for each cell.

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Dashboard Pages](#dashboard-pages)
- [Testing](#testing)
- [Author](#author)

## Project Structure


.
├── app.py                  # Flask application  
├── streamlit_app.py        # Streamlit application  
├── test_app.py             # Unit tests for Flask application  
├── requirements.txt        # Python dependencies  
├── packages.txt            # System packages required  
├── Procfile                # Command to run the application  
├── battery_database.db     # SQLite database file  
└── README.md               # This file  


## Features

- Displays State of Health (SoH) for different Li-ion cells.
- Provides Voltage, Current, Temperature, and Capacity over time graphs for each cell.
- REST API for accessing battery data.
- Unit tests for ensuring code reliability.

## Technologies Used

- **Flask**: Backend framework for serving the REST API.
- **Streamlit**: Frontend framework for creating the interactive dashboard.
- **SQLite**: Database for storing battery data.
- **Plotly**: Library for creating interactive charts.
- **requests**: Library for making HTTP requests to the Flask API.
- **unittest**: Framework for writing and running tests.

## Setup and Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/battery-data-dashboard.git
    cd battery-data-dashboard
    ```

2. **Install system packages**:
    ```bash
    sudo apt-get install -y libgl1 freeglut3-dev libgtk2.0-dev libgl1-mesa-glx
    ```

3. **Set up a virtual environment and install Python dependencies**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Running the Project

1. **Run the Flask API**:
    ```bash
    python app.py
    ```

2. **Run the Streamlit dashboard**:
    ```bash
    streamlit run streamlit_app.py
    ```

### Procfile

For deploying on platforms like Railway, include the following in your `Procfile`:
```
web: streamlit run streamlit_app.py --server.port $PORT
```

## API Endpoints

- **GET /data/<cell_id>**: Get all data for a specific cell ID.
- **GET /soh/<cell_id>**: Get the State of Health for a specific cell ID.
- **GET /cells**: Get a list of all cell IDs.
- **GET /voltage/<cell_id>**: Get voltage vs. time data for a specific cell ID.
- **GET /current/<cell_id>**: Get current vs. time data for a specific cell ID.
- **GET /temperature/<cell_id>**: Get temperature vs. time data for a specific cell ID.
- **GET /capacity/<cell_id>**: Get capacity vs. time data for a specific cell ID.

## Dashboard Pages

### Dashboard Overview

- **State of Health (SoH)**: Displays SoH for the first two cells using pie charts.

### Cell Details

- **Voltage vs. Time**: Line chart showing voltage over time.
- **Current vs. Time**: Line chart showing current over time.
- **Temperature vs. Time**: Line chart showing temperature over time.
- **Capacity vs. Time**: Line chart showing capacity over time.

## Testing

To run the unit tests for the Flask API, use:
```bash
python test_app.py
```

## Author

- **Name**: Raghavendran S.
- **Contact**: [raghavendranhp@gmail.com](mailto:raghavendranhp@gmail.com)
- **Location**: Erode, Tamil Nadu

Feel free to reach out for any questions or collaboration opportunities!

