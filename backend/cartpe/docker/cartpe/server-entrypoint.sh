#!/bin/sh

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py update_index

echo "Db is ready"

gunicorn cartpe.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

# for debug
#python manage.py runserver 0.0.0.0:8000