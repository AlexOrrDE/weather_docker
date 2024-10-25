# Weather Data Ingestion & Processing using Docker

This is a personal project aimed at learning Docker by building an application that automates the ingestion, processing, and storage of weather data. The weather data is collected from the OpenWeather API, processed, and stored in a PostgreSQL database.

## Features

- **Weather Data Ingestion**: Fetches current weather data for a specified city.
- **Data Processing**: Parses and transforms raw JSON data to fit the database schema.
- **Data Storage**: Inserts processed data into a PostgreSQL database.
- **Automated with Docker**: Runs as a Docker container with a scheduled cron job for periodic data ingestion.
- **Fully Tested**: All functions are unit tested to ensure reliability.

## Project Structure

- `src/`
    - `ingestion/`: Scripts for fetching weather data and saving raw data to JSON files.
        - `fetch_weather.py`: Calls the OpenWeather API to fetch weather data.
        - `save_to_json.py`: Saves raw weather data to JSON files for processing.

    - `processing/`: Scripts for reading, transforming, and saving processed data.
        - `read_json.py`: Reads JSON data from the specified directory.
        - `process_data.py`: Transforms the raw JSON data into a format compatible with the database.
        - `save_to_db.py`: Inserts processed data into the PostgreSQL database.

    - `db_connection/`: Defines the connection and handles connection errors for the used database.
        - `connection.py`: Connects to the database using variables specified in .env file.
        - `error_handling.py`: Decorator for handling connection errors.

    - `handler.py`: Executes functions and handles raised errors.

- `test/`: Contains tests for all functions.

- `.env`: Stores environment variables, including API keys and database credentials.
- `Dockerfile`: Defines the container environment and application setup.
- `docker-compose.yml`: Configures and orchestrates container services for easy setup.
- `crontab`: Scedules task for cron jobs to automate data ingestion processes at specified intervals.
- `entrypoint.sh`: Script to start the cron job for automated data ingestion.
- `Makefile`:

## How It Works

1. **Handler Function**: The main function `handler()` manages the data ingestion and processing pipeline. It:
   - Fetches weather data for a given city from the OpenWeather API.
   - Saves raw data in JSON format.
   - Processes JSON data and stores it in the PostgreSQL database.

2. **Docker & Docker-Compose**: The project is containerized for portability and includes a cron job scheduled with Docker for regular data ingestion.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.
- OpenWeather API key (sign up at [OpenWeather](https://openweathermap.org/) for an API key).
- PostgreSQL database (or use a PostgreSQL Docker container if not installed locally).

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AlexOrrDE/weather_docker
   cd weather_docker
   ```


