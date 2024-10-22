import unittest
from src.processing.process_data import process_data


class TestProcessData(unittest.TestCase):

    def test_process_data_success(self):
        """Test that process_data correctly processes valid input."""

        data_list = [
            {
                "name": "Nairobi",
                "main": {"temp": 280.15, "humidity": 80},
                "weather": [{"description": "clear sky"}],
                "dt": 1735128000,
            },
            {
                "name": "Johannesburg",
                "main": {"temp": 295.15, "humidity": 50},
                "weather": [{"description": "light rain"}],
                "dt": 1735084800,
            },
        ]

        expected_output = [
            {
                "city_name": "Nairobi",
                "temperature_celsius": 7.00,
                "humidity": 80,
                "weather_description": "clear sky",
                "datetime": "2024-12-25 13:00:00",
            },
            {
                "city_name": "Johannesburg",
                "temperature_celsius": 22.00,
                "humidity": 50,
                "weather_description": "light rain",
                "datetime": "2024-12-25 01:00:00",
            },
        ]

        processed_data = process_data(data_list)
        self.assertEqual(processed_data, expected_output)

    def test_process_data_missing_fields(self):
        """Test process_data with missing fields."""

        data_list = [
            {
                "name": "New Delhi",
                "main": {"temp": None, "humidity": None},
                "weather": [{}],
                "dt": None,
            },
            {
                "name": "Mumbai",
                "main": {"temp": 300.15, "humidity": 60},
                "weather": [{"description": "overcast clouds"}],
                "dt": 1735171200,
            },
        ]

        expected_output = [
            {
                "city_name": "New Delhi",
                "temperature_celsius": None,
                "humidity": None,
                "weather_description": None,
                "datetime": None,
            },
            {
                "city_name": "Mumbai",
                "temperature_celsius": 27.00,
                "humidity": 60,
                "weather_description": "overcast clouds",
                "datetime": "2024-12-26 01:00:00",
            },
        ]

        processed_data = process_data(data_list)
        self.assertEqual(processed_data, expected_output)

    def test_process_data_empty_input(self):
        """Test process_data with empty input."""

        data_list = []
        expected_output = []
        processed_data = process_data(data_list)
        self.assertEqual(processed_data, expected_output)


if __name__ == "__main__":
    unittest.main()
