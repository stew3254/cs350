#!/bin/sh

python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py runserver 0.0.0.0:5000