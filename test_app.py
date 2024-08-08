import unittest
import json
import sqlite3
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

        # Set up the database connection and insert test data
        self.conn = sqlite3.connect('battery_database.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_test_data()

    def tearDown(self):
        # Remove test data after each test
        self.cursor.execute("DELETE FROM battery_data")
        self.conn.commit()
        self.conn.close()

    def create_test_data(self):
        # Create test data
        self.cursor.execute('''INSERT INTO battery_data (cell_id, current, voltage, capacity, temperature, time) 
                               VALUES (1, 0.5, 3.7, 2800, 25, '2024-08-01 00:00:00')''')
        self.conn.commit()

    def test_get_data_by_cell_id(self):
        # Test for the get_data_by_cell_id endpoint
        response = self.app.get('/data/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_soh_by_cell_id(self):
        # Test for the get_soh_by_cell_id endpoint
        response = self.app.get('/soh/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('soh', data)

    def test_get_all_cells(self):
        # Test for the get_all_cells endpoint
        response = self.app.get('/cells')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_voltage_by_cell_id(self):
        # Test for the get_voltage_by_cell_id endpoint
        response = self.app.get('/voltage/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_current_by_cell_id(self):
        # Test for the get_current_by_cell_id endpoint
        response = self.app.get('/current/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_temperature_by_cell_id(self):
        # Test for the get_temperature_by_cell_id endpoint
        response = self.app.get('/temperature/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_capacity_by_cell_id(self):
        # Test for the get_capacity_by_cell_id endpoint
        response = self.app.get('/capacity/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
