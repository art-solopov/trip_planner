from copy import copy
import re

from flask import Blueprint
import sqlalchemy as sa

from .. import db
from ..models import Point


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
