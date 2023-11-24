#!/bin/sh

# Collect static files
python manage.py collectstatic --noinput

# Make superuser for admin page
python manage.py createsuperuser --noinput
# See if anything changes with app like new apps added
python manage.py makemigrations

# Apply database migrations
python manage.py migrate

# Start new app (Should only be uncommetned when adding new app)
# python manage.py startapp social_network app/social_network

# Start server with debug mode
python manage.py runserver 0.0.0.0:8000