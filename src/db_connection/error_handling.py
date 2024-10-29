import logging
from psycopg2 import OperationalError, DatabaseError


def handle_errors(func):
    """Centralised error handling decorator."""

    def wrapper(*args):
        try:
            return func(*args)
        except OperationalError as e:
            logging.error(
                f"OperationalError occurred in '{func.__name__}': {e}")
            raise
        except DatabaseError as e:
            logging.error(f"DatabaseError occurred in '{func.__name__}': {e}")
            raise
        except Exception as e:
            logging.error(
                f"An unexpected error occurred in '{func.__name__}': {e}")
            raise

    return wrapper
