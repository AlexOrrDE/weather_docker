import unittest
from unittest.mock import patch
from src.handler import handler


class TestHandler(unittest.TestCase):

    @patch("src.handler.save_to_db")
    @patch("src.handler.process_data")
    @patch("src.handler.read_json")
    @patch("src.handler.save_to_json")
    @patch("src.handler.fetch_weather_data")
    @patch("src.handler.os.getenv")
    @patch("src.handler.logging")
    def test_handler_success(
        self,
        mock_logging,
        mock_getenv,
        mock_fetch_weather,
        mock_save_json,
        mock_read_json,
        mock_process_data,
        mock_save_to_db,
    ):
        """Test handler function for successful weather data processing."""

        mock_getenv.return_value = "test_api_key"
        mock_fetch_weather.return_value = {"weather": "data"}
        mock_read_json.return_value = [{"json": "data"}]
        mock_process_data.return_value = [{"processed": "data"}]

        handler()

        mock_getenv.assert_called_once_with("OPENWEATHER_API_KEY")
        mock_logging.info.assert_any_call("API Key: test_api_key")

        mock_fetch_weather.assert_called_once_with("Bristol", "test_api_key")

        mock_save_json.assert_called_once_with({"weather": "data"}, "Bristol")

        mock_read_json.assert_called_once_with("/app/data/json")
        mock_process_data.assert_called_once_with([{"json": "data"}])
        mock_save_to_db.assert_called_once_with([{"processed": "data"}])

        mock_logging.info.assert_called_with("Data insertion complete.")

    @patch("src.handler.save_to_db")
    @patch("src.handler.process_data")
    @patch("src.handler.read_json")
    @patch("src.handler.save_to_json")
    @patch("src.handler.fetch_weather_data")
    @patch("src.handler.os.getenv")
    @patch("src.handler.logging")
    def test_handler_fetch_weather_failed(
        self,
        mock_logging,
        mock_getenv,
        mock_fetch_weather,
        mock_save_json,
        mock_read_json,
        mock_process_data,
        mock_save_to_db,
    ):
        """Test handler when fetching weather data fails."""

        mock_getenv.return_value = "test_api_key"

        mock_fetch_weather.return_value = None

        handler()

        mock_getenv.assert_called_once_with("OPENWEATHER_API_KEY")
        mock_logging.info.assert_any_call("API Key: test_api_key")

        mock_fetch_weather.assert_called_once_with("Bristol", "test_api_key")
        mock_logging.error.assert_called_once_with(
            "Failed to fetch weather data for Bristol."
        )

        mock_save_json.assert_not_called()
        mock_read_json.assert_not_called()
        mock_process_data.assert_not_called()
        mock_save_to_db.assert_not_called()

        mock_logging.info.assert_called_with("Data insertion complete.")

    @patch("src.handler.save_to_db")
    @patch("src.handler.process_data")
    @patch("src.handler.read_json")
    @patch("src.handler.save_to_json")
    @patch("src.handler.fetch_weather_data")
    @patch("src.handler.os.getenv")
    @patch("src.handler.logging")
    def test_handler_exception(
        self,
        mock_logging,
        mock_getenv,
        mock_fetch_weather,
        mock_save_json,
        mock_read_json,
        mock_process_data,
        mock_save_to_db,
    ):
        """Test handler function when an exception occurs."""

        mock_getenv.return_value = "test_api_key"
        mock_fetch_weather.side_effect = Exception("Test exception")

        handler()

        mock_logging.error.assert_called_once_with("Error: Test exception")
        mock_save_json.assert_not_called()
        mock_read_json.assert_not_called()
        mock_process_data.assert_not_called()
        mock_save_to_db.assert_not_called()
        mock_logging.info.assert_called_with("Data insertion complete.")


if __name__ == "__main__":
    unittest.main()
