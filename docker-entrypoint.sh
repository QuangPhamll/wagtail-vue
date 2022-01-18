#!/bin/sh

# Collect static files.
python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
python manage.py create_admin_user
python manage.py update_index
python manage.py runserver --insecure 0.0.0.0:8000
#set -xe; gunicorn brahms.wsgi:application --workers 8
