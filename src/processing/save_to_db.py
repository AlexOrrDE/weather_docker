from psycopg2 import sql
from processing.connection import db_connection
from error_handling.error_connection import handle_errors


@handle_errors
def save_to_db(processed_data):
    """Save processed weather data to PostgreSQL database."""

    conn, cursor = db_connection()

    insert_query = """INSERT INTO weather_data (city_name, temperature_celsius, humidity, weather_description, datetime) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (city_name, datetime)
                DO NOTHING"""

    for entry in processed_data:
        cursor.execute(
            sql.SQL(insert_query),
            (
                entry["city_name"],
                entry["temperature_celsius"],
                entry["humidity"],
                entry["weather_description"],
                entry["datetime"],
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()
