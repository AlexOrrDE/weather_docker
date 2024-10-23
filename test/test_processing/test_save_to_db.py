import unittest
from psycopg2 import sql
from unittest.mock import patch, MagicMock
from src.processing.save_to_db import save_to_db  # Import your save_to_db function


class TestSaveToDb(unittest.TestCase):

    @patch("src.processing.save_to_db.db_connection")  # Mock the db_connection function
    def test_save_to_db_single_entry(self, mock_db_connection):
        """Test save_to_db with a single entry of processed data."""

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_connection.return_value = (mock_conn, mock_cursor)

        processed_data = [
            {
                "city_name": "New York",
                "temperature_celsius": 20.5,
                "humidity": 70,
                "weather_description": "Clear sky",
                "datetime": "2024-10-22 10:00:00",
            }
        ]

        save_to_db(processed_data)

        insert_query = """INSERT INTO weather_data (city_name, temperature_celsius, humidity, weather_description, datetime) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (city_name, datetime)
                DO NOTHING"""

        mock_cursor.execute.assert_called_once_with(
            sql.SQL(insert_query),
            ("New York", 20.5, 70, "Clear sky", "2024-10-22 10:00:00"),
        )

        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("src.processing.save_to_db.db_connection")
    def test_save_to_db_multiple_entries(self, mock_db_connection):
        """Test save_to_db with multiple entries of processed data."""

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_connection.return_value = (mock_conn, mock_cursor)

        processed_data = [
            {
                "city_name": "New York",
                "temperature_celsius": 20.5,
                "humidity": 70,
                "weather_description": "Clear sky",
                "datetime": "2024-10-22 10:00:00",
            },
            {
                "city_name": "Los Angeles",
                "temperature_celsius": 25.0,
                "humidity": 60,
                "weather_description": "Sunny",
                "datetime": "2024-10-22 12:00:00",
            },
        ]

        save_to_db(processed_data)

        insert_query = """INSERT INTO weather_data (city_name, temperature_celsius, humidity, weather_description, datetime) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (city_name, datetime)
                DO NOTHING"""

        self.assertEqual(mock_cursor.execute.call_count, 2)

        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("src.processing.save_to_db.db_connection")
    def test_save_to_db_handles_errors(self, mock_db_connection):
        """Test that save_to_db handles database errors correctly."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_connection.return_value = (mock_conn, mock_cursor)

        mock_cursor.execute.side_effect = Exception("Database error")

        processed_data = [
            {
                "city_name": "New York",
                "temperature_celsius": 20.5,
                "humidity": 70,
                "weather_description": "Clear sky",
                "datetime": "2024-10-22 10:00:00",
            }
        ]

        with self.assertRaises(Exception):
            save_to_db(processed_data)

        mock_conn.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
