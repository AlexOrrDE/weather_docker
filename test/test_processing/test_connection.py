import unittest
from unittest.mock import patch, MagicMock
from src.processing.connection import db_connection


class TestDbConnection(unittest.TestCase):

    @patch("psycopg2.connect")
    @patch("os.getenv")
    def test_db_connection_success(self, mock_getenv, mock_connect):
        """Test successful database connection."""

        mock_getenv.side_effect = lambda key: {
            "DB_NAME": "test_db",
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_password",
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
        }.get(key)

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        conn, cursor = db_connection()

        mock_connect.assert_called_once_with(
            dbname="test_db",
            user="test_user",
            password="test_password",
            host="localhost",
            port="5432",
        )

        self.assertTrue(mock_conn.autocommit)

        self.assertEqual(conn, mock_conn)
        self.assertEqual(cursor, mock_cursor)


if __name__ == "__main__":
    unittest.main()
