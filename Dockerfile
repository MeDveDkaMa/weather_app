FROM alpine

WORKDIR /home/data
COPY ./ /home/data/

RUN apk add python3 && apk add py3-pip && pip install -r requirements.txt --ignore-installed && python3 manage.py makemigrations && python3 manage.py migrate

EXPOSE 8000

CMD python3 manage.py runserver 0.0.0.0:8000

