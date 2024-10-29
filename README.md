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
- `Makefile`: Automates setup and execution of various development tasks, including environment creation, dependency installation, and running tests.

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

2. **Setup Postgres database and table**:

- Setup a Postgres database.
- In this database, create a table with name: **weather_data**

3. **Setup Environment Variables**:

Create a .env file in your repository and set your OpenWeather API key and PostgreSQL credentials.

- Example .env:

        OPENWEATHER_API_KEY=your_api_key
        DB_NAME=your_db_name
        DB_USER=your_user
        DB_PASSWORD=your_password
        DB_HOST=host.docker.internal
        DB_PORT=5432

4. **Build and Run**:

Use the Makefile to set up the project environment and run necessary tasks.

- To create the Python environment and install requirements, run:

```bash
make all
```

- This command will:

    - Create a virtual environment.
    - Install the required Python packages listed in requirements.txt.
    - Set up development tools (Bandit, Safety, Flake8, Coverage).
    - Run security tests, flake8 checks, unit tests, and coverage checks.

- To build the Docker image and start the container, run:

```bash
docker-compose up -d --build
```

The application will run on build, and then periodically depending on the frequency specified in `crontab` (by default this is every twenty minutes from the hour).

- To stop the container, run:
```bash
docker-compose down
```

## Troubleshooting

- **Environment Variables**: Ensure the .env file is correctly configured.
- **Docker Logs**: Check logs in Docker, or by running:
```bash
docker logs weather-ingestor
```
- **Run Tests**: Check logs in terminal after running:
```bash
make run-unit-tests
```

## Future Improvements

- Add table of contents to `README.md`
- Add more cities and expand data processing capabilities.
- Implement database and table setup into `Makefile`.
- Implement improved error handling and data validation.
- Set up monitoring for the database and application.