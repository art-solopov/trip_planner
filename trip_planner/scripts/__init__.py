from copy import copy
import re

from flask import Blueprint
import sqlalchemy as sa

from .. import db
from ..models import Point, Trip


scripts = Blueprint('scripts', __name__)

_time_search = re.compile(r'\A(\d{1,2}):(\d{1,2})\Z')


@scripts.cli.command('reformat_schedule_dates')
def reformat_schedule_dates():
    points_with_schedule = Point.query.filter(
        Point.schedule.cast(sa.Text) != '{}'
    )
    for point in points_with_schedule:
        print(f'Processing point {point.name}')
        new_schedule = {}
        for wday, times in point.schedule.items():
            new_schedule[wday] = copy(times)
            for k in ['open_from', 'open_to']:
                time = times.get(k, '')
                time_match = _time_search.match(time)
                if time_match:
                    hour = int(time_match[1])
                    minute = int(time_match[2])
                    new_time = f'{hour:02d}:{minute:02d}'
                    new_schedule[wday][k] = new_time
        point.schedule = new_schedule
        db.session.add(point)
    db.session.commit()


@scripts.cli.command('calculate_center_coordinates')
def calculate_center_coordinates():
    query = Trip.query.join(Trip.points) \
        .group_by(Trip.id) \
        .add_columns(
            db.func.avg(Point.lat).label('center_lat'),
            db.func.avg(Point.lon).label('center_lon')
            )
    for row in query:
        trip = row.Trip
        trip.center_lat = row.center_lat
        trip.center_lon = row.center_lon
        db.session.add(trip)

    db.session.commit()


@scripts.cli.command('add_key_to_trips')
def add_key_to_trips():
    query = Trip.query.filter_by(key=None)
    for trip in query:
        trip.key = Trip.generate_key()
        db.session.add(trip)
    db.session.commit()
