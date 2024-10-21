from datetime import datetime, timedelta


def process_data(data_list):
    """Processes read JSON data."""

    processed_data = []
    for data in data_list:
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]

        # Convert temperature to celsius
        temperature_kelvin = main.get("temp")
        temperature_celsius = (
            temperature_kelvin - 273.15 if temperature_kelvin is not None else None
        )

        # Convert timestamp to data & time
        timestamp_unix = data.get("dt")
        if timestamp_unix is not None:
            timestamp_local = datetime.fromtimestamp(timestamp_unix) + timedelta(
                hours=1
            )
            timestamp_formatted = timestamp_local.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp_formatted = None

        processed_entry = {
            "city_name": data.get("name"),
            "temperature_celsius": (
                round(temperature_celsius, 2)
                if temperature_celsius is not None
                else None
            ),
            "humidity": main.get("humidity"),
            "weather_description": weather.get("description"),
            "datetime": timestamp_formatted,
        }

        processed_data.append(processed_entry)

    return processed_data
