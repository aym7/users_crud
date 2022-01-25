FROM python:3.8

# Useful to get logs
ENV PYTHONUNBUFFERED 1

# Specifies a working directory
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["bash", "/app/docker-entrypoint.sh"]

# Copy all the files to the app directory
COPY . /app

