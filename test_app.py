import unittest
import json
import sqlite3
import os
from app import app

class FlaskTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the database connection once for all tests
        cls.conn = sqlite3.connect('battery_database.db')
        cls.conn.row_factory = sqlite3.Row
        cls.cursor = cls.conn.cursor()
        cls.backup_original_data()
        cls.create_test_data()

    @classmethod
    def tearDownClass(cls):
        # Restore the original data after all tests
        cls.restore_original_data()
        cls.conn.close()

    @classmethod
    def backup_original_data(cls):
        # Back up the original data
        cls.cursor.execute('SELECT * FROM battery_data')
        cls.original_data = cls.cursor.fetchall()

    @classmethod
    def restore_original_data(cls):
        # Restore the original data
        cls.cursor.execute("DELETE FROM battery_data")
        cls.conn.commit()
        for row in cls.original_data:
            cls.cursor.execute('''INSERT INTO battery_data (cell_id, current, voltage, capacity, temperature, time)
                                  VALUES (?, ?, ?, ?, ?, ?)''', 
                                  (row['cell_id'], row['current'], row['voltage'], row['capacity'], row['temperature'], row['time']))
        cls.conn.commit()

    @classmethod
    def create_test_data(cls):
        # Insert test data
        cls.cursor.execute('''INSERT INTO battery_data (cell_id, current, voltage, capacity, temperature, time) 
                               VALUES (9999, 0.5, 3.7, 2800, 25, '2024-08-01 00:00:00')''')
        cls.conn.commit()

    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

    def test_get_data_by_cell_id(self):
        # Test for the get_data_by_cell_id endpoint
        response = self.app.get('/data/9999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_soh_by_cell_id(self):
        # Test for the get_soh_by_cell_id endpoint
        response = self.app.get('/soh/9999')
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
        response = self.app.get('/voltage/9999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_current_by_cell_id(self):
        # Test for the get_current_by_cell_id endpoint
        response = self.app.get('/current/9999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_temperature_by_cell_id(self):
        # Test for the get_temperature_by_cell_id endpoint
        response = self.app.get('/temperature/9999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_get_capacity_by_cell_id(self):
        # Test for the get_capacity_by_cell_id endpoint
        response = self.app.get('/capacity/9999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
