import requests
import logging

logging.getLogger().setLevel(logging.INFO)


def fetch_weather_data(city, api_key):
    """Fetch weather data from the Openweather API."""

    if api_key is None:
        raise ValueError(
            "API key not found. "
            "Make sure the OPENWEATHER_API_KEY environment variable is set."
        )

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city},GB&appid={api_key}"
    )
    logging.info(f"Request URL: {url}")

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error fetching data from API: {response.status_code}")
        return None
