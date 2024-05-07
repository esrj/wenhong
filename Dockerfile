FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install Django Pillow mysqlclient

COPY . /code/

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"]


