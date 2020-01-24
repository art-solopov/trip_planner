from typing import Sequence, Tuple
import re

from ..data import MapData
from ..models import Point

ScheduleRow = Tuple[str, str, str, str]


_schedule_line_re = re.compile(r'(?P<dowfrom>\w+)(?:-(?P<dowto>\w+))?\s+'
                               r'(?P<timefrom>\d+(?::\d{2})?)-'
                               r'(?P<timeto>\d+(?::\d{2})?)')


def _normalize_timestring(ts: str) -> str:
    if ':' in ts:
        return ts
    else:
        return f"{ts}:00"


def _parse_schedule_row(schedule_row: str) -> ScheduleRow:
    m = _schedule_line_re.fullmatch(schedule_row)
    if m is None:
        return
    dowfrom, dowto, timefrom, timeto = m.groups()
    timefrom, timeto = map(_normalize_timestring, (timefrom, timeto))
    return (dowfrom, dowto, timefrom, timeto)


class PointData(MapData):
    def __init__(self, point: Point):
        self.point = point

    @property
    def point_map_url(self) -> str:
        return super().point_map_url((self.point.lat, self.point.lon))

    @property
    def notes_lines(self) -> Sequence[str]:
        return [l for l in self.point.notes.splitlines() if l]

    @property
    def schedule(self) -> Sequence[ScheduleRow]:
        return filter(bool,
                      (_parse_schedule_row(row)
                       for row in self.point.schedule.splitlines()))
