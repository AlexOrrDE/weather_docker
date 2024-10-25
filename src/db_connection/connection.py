import os
import psycopg2
from src.db_connection.error_handling import handle_errors


@handle_errors
def db_connection():
    """Connect to Postgres database."""

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )

    conn.autocommit = True
    cursor = conn.cursor()
    return conn, cursor
