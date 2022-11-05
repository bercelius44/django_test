# Delivery scheduler

REST API using Django and Django Rest Framework

Features:

1. Schedule an order to a driver for a date and time specifying its pickup and delivery place(lat,lng).
2. Get all orders scheduled in a specific day.
3. Get all orders a driver has in a specific day.
4. Get the closest driver to a location in a specific date and time.

## Installation

Clone the repository, with Python3 create a virtual env in the same folder the repository is and activate it.

    .
    ├── Repository Folder
    └── venv

For Windows

```bash
python -m venv ./venv
venv\Scripts\activate
```

Now, you have to install the packages listed in the requirements.txt using pip.

```bash
pip install Django==4.1.3
pip install djangorestframework==3.14.0
pip install apscheduler==3.9.1
pip install requests==2.28.1
pip install drf-spectacular==0.24.2
```

Go to the api folder and run the API.

```bash
python manage.py runserver 0.0.0.0:8000
```

For running test.

```bash
python manage.py test
```

For the API doc, once Django is running go to.

```browser
http://localhost:8000
```

## Installation with Docker

Clone the repository, go to the repository folder and run this commands.

```bash
docker build -t django_test .
docker run -d -p 8000:8000 --name django django_test
```

For the API doc, once Django container is running go to.

```browser
http://localhost:8000
```
