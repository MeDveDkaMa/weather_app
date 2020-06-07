#!/bin/bash
pwd
python3.7 -m virtualenv env
source env/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver