FROM python:3.7.9-alpine

WORKDIR /home/data
COPY ./ /home/data/

RUN pip install -r requirements.txt --ignore-installed && python manage.py makemigrations && python manage.py migrate

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000

