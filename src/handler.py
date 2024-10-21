import os
import logging
from ingestion.fetch_weather import fetch_weather_data
from ingestion.save_to_json import save_to_json
from processing.read_json import read_json
from processing.process_data import process_data
from processing.save_to_db import save_to_db

logging.getLogger().setLevel(logging.INFO)


def handler():
    """Handler function to ingest and process the weather data."""

    try:
        city = "Bristol"
        api_key = os.getenv("OPENWEATHER_API_KEY")
        logging.info(f"API Key: {api_key}")

        weather_data = fetch_weather_data(city, api_key)
        if weather_data:
            save_to_json(weather_data, city)
        else:
            logging.error(f"Failed to fetch weather data for {city}.")

        data_dir = "/app/data/json"

        json_data = read_json(data_dir)
        processed_data = process_data(json_data)
        save_to_db(processed_data)

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        logging.info("Data insertion complete.")


if __name__ == "__main__":
    handler()
