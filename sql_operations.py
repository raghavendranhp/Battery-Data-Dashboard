# Importing necessary libraries for database operations and data manipulation
import mysql.connector
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

# Function to connect to the SQLite database
def get_connections():
    try:
        # Establish connection to SQLite database
        connection1 = sqlite3.connect('battery_database.db')
        # Create a cursor object using the connection
        curs1 = connection1.cursor()
        # Create an engine object for SQLAlchemy
        engine = create_engine('sqlite:///battery_database.db', echo=True)
        return connection1, curs1, engine
    except Exception as e:
        # Print an error message if the connection fails
        print(f"Error occurred while connecting to SQL: {str(e)}")

# Function to close the database connections
def close_connections(curs1, connection1):
    try:
        # Close the cursor and the connection
        curs1.close()
        connection1.close()
    except Exception as e:
        # Print an error message if closing the connections fails
        print(f"Error occurred while closing cursor and connection: {str(e)}")

# Function to create the table in the SQLite database
def table_creation_sql():
    try:
        # SQL query to create the battery_data table if it doesn't already exist
        table_creation_query = '''
        CREATE TABLE IF NOT EXISTS battery_data (
            cell_id INTEGER,
            current REAL,
            voltage REAL,
            capacity REAL,
            temperature REAL,
            time TEXT
        )'''
        # Get database connections
        connection1, curs1, engine = get_connections()
        # Execute the table creation query
        curs1.execute(table_creation_query)
        # Close the database connections
        close_connections(curs1, connection1)
    except Exception as e:
        # Print an error message if table creation fails
        print(f"Error while creating table: {str(e)}")

# Function to insert data into the SQLite database
def insert_to_sql(final_df):
    try:
        # Get database connections
        connection1, curs1, engine = get_connections()
        # Insert the dataframe into the battery_data table
        final_df.to_sql('battery_data', engine, if_exists='append', index=False)
        print("Details inserted successfully!")
        # Close the database connections
        close_connections(curs1, connection1)
    except IntegrityError:
        # Print a message if the data is already inserted
        print('Table values already inserted')

# Read the Excel file into a Pandas dataframe
final_df = pd.read_excel(r"C:\Users\ksund\Music\Nunam\combined_data.xlsx")
# Check the shape of the dataframe to ensure it was read correctly
#final_df.shape
# Create the table in the database
table_creation_sql()
# Insert the data from the dataframe into the database
insert_to_sql(final_df)
