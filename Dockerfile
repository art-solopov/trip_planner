FROM python:3.7

ARG uid=1100

RUN apt-get update && apt-get -y install postgresql-client-11

RUN useradd -u $uid -s /bin/bash -m trip_planner

USER trip_planner

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

ENV FLASK_APP=trip_planner
ENV INSTANCE_PATH=/instance

VOLUME ["/app/tmp", "/app/log", "/instance"]

CMD ["/home/trip_planner/.local/bin/gunicorn", "-c", "gunicorn.config.py", "trip_planner:create_app()"]