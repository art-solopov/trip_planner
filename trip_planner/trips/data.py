from typing import Sequence, Tuple, Dict

from markupsafe import Markup, escape

from ..data import MapData
from ..models import Point
from .forms import ScheduleField


class PointScheduleData:
    WEEKDAYS = ScheduleField.WEEKDAYS

    def __init__(self, point: Point):
        self.schedule = point.schedule

    def __call__(self):
        return Markup(''.join(self._schedule_rows()))

    def _schedule_rows(self):
        yield '<table class="schedule-table">'

        for wday in self.WEEKDAYS:
            weekday_data = self.schedule.get(wday)
            if weekday_data is not None:
                yield self.schedule_row(wday, weekday_data)

        yield '</table>'

    @staticmethod
    def schedule_row(day_of_week: str, data: Dict[str, str]):
        day_of_week = escape(day_of_week)
        open_from = escape(data['open_from'])
        open_to = escape(data['open_to'])
        return ('<tr>' +
                f'<th class="{day_of_week}">{day_of_week.capitalize()}</th>' +
                f'<td>{open_from}–{open_to}</td>' +
                '</tr>')


class PointData(MapData):
    def __init__(self, point: Point):
        self.point = point
        self.schedule = PointScheduleData(point)

    @property
    def point_map_url(self) -> str:
        return super().point_map_url((self.point.lat, self.point.lon))

    @property
    def notes_lines(self) -> Sequence[str]:
        return [l for l in self.point.notes.splitlines() if l]
