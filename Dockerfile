FROM python:3

RUN apt-get update -y

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


RUN mkdir /app
WORKDIR /app
COPY ./api /app

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]