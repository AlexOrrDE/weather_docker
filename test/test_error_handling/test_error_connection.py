import unittest
from unittest.mock import patch
from psycopg2 import OperationalError, DatabaseError
from src.error_handling.error_connection import handle_errors


class TestHandleErrors(unittest.TestCase):

    @patch("src.error_handling.error_connection.logging.error")
    def test_operational_error_handling(self, mock_log_error):
        """Test if OperationalError is caught, logged, and re-raised."""

        @handle_errors
        def faulty_func():
            raise OperationalError("Operational error occurred")

        with self.assertRaises(OperationalError):
            faulty_func()

        mock_log_error.assert_called_once_with(
            "OperationalError occurred in 'faulty_func': Operational error occurred"
        )

    @patch("src.error_handling.error_connection.logging.error")
    def test_database_error_handling(self, mock_log_error):
        """Test if DatabaseError is caught, logged, and re-raised."""

        @handle_errors
        def faulty_func():
            raise DatabaseError("Database error occurred")

        with self.assertRaises(DatabaseError):
            faulty_func()

        mock_log_error.assert_called_once_with(
            "DatabaseError occurred in 'faulty_func': Database error occurred"
        )

    @patch("src.error_handling.error_connection.logging.error")
    def test_general_exception_handling(self, mock_log_error):
        """Test if general exceptions are caught, logged, and re-raised."""

        @handle_errors
        def faulty_func():
            raise ValueError("General error occurred")

        with self.assertRaises(ValueError):
            faulty_func()

        mock_log_error.assert_called_once_with(
            "An unexpected error occurred in 'faulty_func': General error occurred"
        )


if __name__ == "__main__":
    unittest.main()
