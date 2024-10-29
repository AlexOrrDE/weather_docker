import unittest
import json
from unittest.mock import patch, mock_open, call
from src.ingestion.save_to_json import save_to_json


class TestSaveToJson(unittest.TestCase):

    @patch("os.makedirs")
    @patch("os.path.exists", return_value=False)
    @patch("builtins.open", new_callable=mock_open)
    def test_save_to_json_creates_directories_and_file(
        self, mock_open_fn, mock_exists, mock_makedirs
    ):
        """
        Test if the function creates the directories
        and saves data as JSON.
        """

        data = {"weather": "sunny", "temperature": 25}
        city = "London"

        save_to_json(data, city)

        mock_makedirs.assert_has_calls([call("data"), call("data/json")])

        expected_file_path = "/app/data/json/London_weather_"
        self.assertTrue(mock_open_fn.called)

        file_path_arg = mock_open_fn.call_args[0][0]
        self.assertTrue(file_path_arg.startswith(expected_file_path))

        handle = mock_open_fn()
        written_data = "".join(call.args[0]
                               for call in handle.write.call_args_list)
        expected_data = json.dumps(data, indent=4)
        self.assertEqual(written_data, expected_data)

    @patch("os.makedirs")
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_save_to_json_does_not_create_directories_if_exist(
        self, mock_open_fn, mock_exists, mock_makedirs
    ):
        """
        Test if the function skips directory creation
        when they already exist.
        """

        data = {"weather": "rainy", "temperature": 18}
        city = "Paris"

        save_to_json(data, city)

        mock_makedirs.assert_not_called()

        expected_file_path = "/app/data/json/Paris_weather_"
        file_path_arg = mock_open_fn.call_args[0][0]
        self.assertTrue(file_path_arg.startswith(expected_file_path))

        handle = mock_open_fn()
        written_data = "".join(call.args[0]
                               for call in handle.write.call_args_list)
        expected_data = json.dumps(data, indent=4)
        self.assertEqual(written_data, expected_data)


if __name__ == "__main__":
    unittest.main()
