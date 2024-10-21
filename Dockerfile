FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app
COPY . /app


RUN pip install requests psycopg2-binary

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY crontab /etc/cron.d/weather-cron
RUN chmod 0644 /etc/cron.d/weather-cron
RUN crontab /etc/cron.d/weather-cron
RUN touch /var/log/cron.log

ENTRYPOINT ["/app/entrypoint.sh"]