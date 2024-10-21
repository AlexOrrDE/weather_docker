import os
import json


def read_json(data_dir):
    """Reads ingested JSON data."""

    data_list = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            with open(os.path.join(data_dir, filename), "r") as f:
                data = json.load(f)
                data_list.append(data)

    return data_list
