FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron

WORKDIR /app
COPY . /app
ENV PYTHONPATH="/app"

RUN pip install -r requirements.txt

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

COPY crontab /etc/cron.d/weather-cron
RUN chmod 0644 /etc/cron.d/weather-cron
RUN crontab /etc/cron.d/weather-cron
RUN touch /var/log/cron.log

ENTRYPOINT ["/app/entrypoint.sh"]