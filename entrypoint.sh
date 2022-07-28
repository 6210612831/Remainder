#!/bin/bash

# Prepare log files and start outputting logs to stdout
mkdir -p /code/logs
touch /code/logs/gunicorn.log
touch /code/logs/gunicorn-access.log
touch /code/logs/gunicorn-error.log
tail -n 0 -f /code/logs/gunicorn*.log &

export DJANGO_SETTINGS_MODULE=Remainder.settings


exec gunicorn -c /code/Remainder/gunicorn.py Remainder.wsgi \
"$@"