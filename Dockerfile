FROM python:3.8

# Useful to get logs
ENV PYTHONUNBUFFERED 1

# Specifies a working directory
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

# Copy all the files to the app directory
COPY . /app

# CMD is in docker-compose
# CMD python manage.py runserver 0.0.0.0:8000
