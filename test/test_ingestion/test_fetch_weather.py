import unittest
from unittest.mock import patch, Mock
from src.ingestion.fetch_weather import fetch_weather_data


class TestFetchWeatherData(unittest.TestCase):

    @patch("requests.get")
    def test_fetch_weather_data_success(self, mock_get):
        """Test when API returns a 200 status code with valid data."""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "weather": [{"description": "clear sky"}],
            "main": {"temp": 300},
        }
        mock_get.return_value = mock_response

        api_key = "test_api_key"
        city = "London"
        result = fetch_weather_data(city, api_key)

        mock_get.assert_called_with(
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={city},GB&appid={api_key}"
        )

        self.assertEqual(result["weather"][0]["description"], "clear sky")
        self.assertEqual(result["main"]["temp"], 300)

    @patch("requests.get")
    def test_fetch_weather_data_error(self, mock_get):
        """Test when API returns a non-200 status code."""

        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        api_key = "test_api_key"
        city = "InvalidCity"
        result = fetch_weather_data(city, api_key)

        self.assertIsNone(result)

    def test_fetch_weather_data_no_api_key(self):
        """Test that the function raises an error when API key is None."""
        city = "London"
        api_key = None

        with self.assertRaises(ValueError) as context:
            fetch_weather_data(city, api_key)

        self.assertEqual(
            str(context.exception),
            "API key not found. "
            "Make sure the OPENWEATHER_API_KEY environment variable is set.",
        )


if __name__ == "__main__":
    unittest.main()
