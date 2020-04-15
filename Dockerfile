FROM python:3.7

RUN apt-get update && apt-get -y install postgresql-client-11

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV FLASK_APP=trip_planner
CMD ["gunicorn", "-b", "0.0.0.0:5000", "trip_planner:create_app()"]