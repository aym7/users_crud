#!/bin/bash

# Prepares and apply migrations
python manage.py makemigrations
python manage.py migrate

# Automatically creates a superuser
# Will automatically use environment variables DJANGO_SUPERUSER_<field> to create the superuser
# NB: will display an errorline if the user already exists
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser --noinput
fi

# Starts server
python manage.py runserver 0.0.0.0:8000

