from typing import Sequence, Dict

from markupsafe import Markup, escape

from trip_planner.data import MapData
from trip_planner.models import Point
from trip_planner.bs_classes import ScheduleClasses


class PointScheduleData:
    WEEKDAYS = 'mon tue wed thu fri sat sun'.split()

    COMMON_CELL_CLASS = ScheduleClasses.CELL_CLASS
    COMMON_WDAY_CLASS = ScheduleClasses.COMMON_WEEKDAY_CLASS
    WDAY_CLASSES = ScheduleClasses.WEEKDAYS

    def __init__(self, point: Point):
        self.schedule = point.schedule

    def __call__(self):
        return Markup(''.join(self._schedule_rows()))

    @classmethod
    def weekday_cell(cls, day_of_week: str):
        dow_class = ' '.join([
            cls.COMMON_CELL_CLASS,
            cls.COMMON_WDAY_CLASS,
            cls.WDAY_CLASSES.get(day_of_week, cls.WDAY_CLASSES['_default'])
        ])
        day_of_week = escape(day_of_week).capitalize()
        return f'<th class="{dow_class}">{day_of_week}</th>'

    def _schedule_rows(self):
        yield '<table class="schedule-table">'

        for wday in self.WEEKDAYS:
            weekday_data = self.schedule.get(wday)
            if weekday_data is not None:
                yield self._schedule_row(wday, weekday_data)

        yield '</table>'

    @classmethod
    def _schedule_row(cls, day_of_week: str, data: Dict[str, str]):
        open_from = escape(data['open_from'])
        open_to = escape(data['open_to'])
        if open_from and open_to:
            schedule_text = f'{open_from}–{open_to}'
        else:
            schedule_text = '—'
        return ('<tr>' +
                cls.weekday_cell(day_of_week) +
                f'<td class="{cls.COMMON_CELL_CLASS}">{schedule_text}</td>' +
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
