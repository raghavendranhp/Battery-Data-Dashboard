from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('battery_database.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

# Endpoint to get all data for a specific cell_id
@app.route('/data/<int:cell_id>', methods=['GET'])
def get_data_by_cell_id(cell_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM battery_data WHERE cell_id = ?', (cell_id,))
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify(data)

# Endpoint to get the state of health for a specific cell_id
@app.route('/soh/<int:cell_id>', methods=['GET'])
def get_soh_by_cell_id(cell_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT capacity, voltage FROM battery_data WHERE cell_id = ?', (cell_id,))
    rows = cursor.fetchall()
    conn.close()

    capacities = [row['capacity'] for row in rows]
    nominal_capacity = 3000  # Assuming nominal capacity is 3000
    if capacities:
        soh = (sum(capacities) / len(capacities)) / nominal_capacity * 100
        return jsonify({'cell_id': cell_id, 'soh': soh})
    else:
        return jsonify({'error': 'Cell ID not found'}), 404

# Endpoint to get all cell IDs
@app.route('/cells', methods=['GET'])
def get_all_cells():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT cell_id FROM battery_data')
    rows = cursor.fetchall()
    conn.close()

    cell_ids = [row['cell_id'] for row in rows]
    return jsonify(cell_ids)

# Endpoint to get voltage vs. time data for a specific cell_id
@app.route('/voltage/<int:cell_id>', methods=['GET'])
def get_voltage_by_cell_id(cell_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT time, voltage FROM battery_data WHERE cell_id = ? ORDER BY time', (cell_id,))
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify(data)

# Endpoint to get current vs. time data for a specific cell_id
@app.route('/current/<int:cell_id>', methods=['GET'])
def get_current_by_cell_id(cell_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT time, current FROM battery_data WHERE cell_id = ? ORDER BY time', (cell_id,))
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify(data)

# Endpoint to get temperature vs. time data for a specific cell_id
@app.route('/temperature/<int:cell_id>', methods=['GET'])
def get_temperature_by_cell_id(cell_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT time, temperature FROM battery_data WHERE cell_id = ? ORDER BY time', (cell_id,))
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify(data)

# Endpoint to get capacity vs. time data for a specific cell_id
@app.route('/capacity/<int:cell_id>', methods=['GET'])
def get_capacity_by_cell_id(cell_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT time, capacity FROM battery_data WHERE cell_id = ? ORDER BY time', (cell_id,))
    rows = cursor.fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
