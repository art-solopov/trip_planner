from typing import Sequence, Tuple, Dict

from markupsafe import Markup, escape

from ..data import MapData
from ..models import Point
from .forms import ScheduleField


class PointScheduleData:
    WEEKDAYS = ScheduleField.WEEKDAYS

    COMMON_CELL_CLASS = 'p-2'
    COMMON_WDAY_CLASS = 'font-bold'
    WDAY_CLASSES = {
        '_default': 'bg-black text-white',
        'fri': 'bg-teal-800 text-white',
        'sat': 'bg-orange-300',
        'sun': 'bg-yellow-300'
    }

    def __init__(self, point: Point):
        self.schedule = point.schedule

    def __call__(self):
        return Markup(''.join(self._schedule_rows()))

    def _schedule_rows(self):
        yield '<table class="schedule-table">'

        for wday in self.WEEKDAYS:
            weekday_data = self.schedule.get(wday)
            if weekday_data is not None:
                yield self._schedule_row(wday, weekday_data)

        yield '</table>'

    def _schedule_row(self, day_of_week: str, data: Dict[str, str]):
        day_of_week = escape(day_of_week)
        open_from = escape(data['open_from'])
        open_to = escape(data['open_to'])
        if open_from and open_to:
            schedule_text = f'{open_from}–{open_to}'
        else:
            schedule_text = '—'
        dow_class = ' '.join([
            self.COMMON_CELL_CLASS,
            self.COMMON_WDAY_CLASS,
            self.WDAY_CLASSES.get(day_of_week, self.WDAY_CLASSES['_default'])
        ])
        return ('<tr>' +
                f'<th class="{dow_class}">{day_of_week.capitalize()}</th>' +
                f'<td class="{self.COMMON_CELL_CLASS}">{schedule_text}</td>' +
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
