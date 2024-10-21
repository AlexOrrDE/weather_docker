import os
import json
from datetime import datetime, timedelta


def save_to_json(data, city):
    """Save the fetched data as a JSON file."""

    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/json"):
        os.makedirs("data/json")

    timestamp = (datetime.now() + timedelta(hours=1)).strftime("%Y-%d-%m_%H-%M-%S")
    file_name = f"/app/data/json/{city}_weather_{timestamp}.json"

    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)
