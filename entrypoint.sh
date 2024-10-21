#!/bin/bash

printenv | grep -v "no_proxy" >> /etc/environment

python /app/src/handler.py >> /var/log/weather_ingestion.log 2>&1

cron && tail -f /var/log/cron.log
