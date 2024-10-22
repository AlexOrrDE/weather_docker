import unittest
import json
from unittest import mock
from src.processing.read_json import read_json


class TestReadJson(unittest.TestCase):

    @mock.patch("os.listdir")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_read_json_success(self, mock_open, mock_listdir):
        """Test that read_json correctly reads JSON files."""

        mock_listdir.return_value = ["file1.json", "file2.json"]

        mock_open.side_effect = [
            mock.mock_open(read_data='{"key": "value1"}').return_value,
            mock.mock_open(read_data='{"key": "value2"}').return_value,
        ]

        expected_output = [{"key": "value1"}, {"key": "value2"}]

        result = read_json("mock_directory")
        self.assertEqual(result, expected_output)
        self.assertEqual(mock_open.call_count, 2)

    @mock.patch("os.listdir")
    def test_read_json_no_json_files(self, mock_listdir):
        """Test read_json with no JSON files in the directory."""

        mock_listdir.return_value = ["file1.txt", "file2.txt"]

        result = read_json("mock_directory")
        self.assertEqual(result, [])

    @mock.patch("os.listdir")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_read_json_invalid_json(self, mock_open, mock_listdir):
        """Test read_json with an invalid JSON file."""

        mock_listdir.return_value = ["invalid.json"]

        mock_open.return_value.__enter__.return_value.read.side_effect = [
            "invalid json"
        ]

        with self.assertRaises(json.JSONDecodeError):
            read_json("mock_directory")

    @mock.patch("os.listdir")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_read_json_empty_directory(self, mock_open, mock_listdir):
        """Test read_json with an empty directory."""

        mock_listdir.return_value = []

        result = read_json("mock_directory")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
