#!/bin/sh
echo "Hello world!"
# while ! nc -z db 3306 ; do
#     echo "Waiting for the MySQL Server"
#     sleep 3
# done

# Removes all data from the database
# python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate

# uvicorn cycrent.asgi:application --reload
python manage.py runserver 0.0.0.0:8000