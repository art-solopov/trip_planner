from typing import Sequence, Dict, Generic, TypeVar

from markupsafe import Markup, escape

from trip_planner.data import MapData
from trip_planner.models import Point, Trip, User, PrivacyStatusEnum, WithPrivacyOptions
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


class PrivacyStatusPresenter:
    # TODO: replace with i18n
    TITLES = {
            PrivacyStatusEnum.private: 'Private',
            PrivacyStatusEnum.public: 'Public'
            }

    ICONS = {
            PrivacyStatusEnum.private: 'file-lock-fill',
            PrivacyStatusEnum.public: 'eye'
            }

    ACTION_ICONS = {
        'make_private': ICONS[PrivacyStatusEnum.private],
        'make_public': ICONS[PrivacyStatusEnum.public]
    }

    def __init__(self, privacy_status: PrivacyStatusEnum):
        self.privacy_status = privacy_status

    @property
    def title(self):
        return self.TITLES[self.privacy_status]

    @property
    def icon(self):
        return self.ICONS[self.privacy_status]


T = TypeVar('T', bound=WithPrivacyOptions)


class BaseData(Generic[T]):
    def __init__(self, obj: T):
        self._object = obj
        self.privacy_status = PrivacyStatusPresenter(obj.privacy_status)

    def __getattr__(self, name):
        return getattr(self._object, name)


class PointData(MapData, BaseData[Point]):
    def __init__(self, point: Point):
        super().__init__(point)
        self.schedule = PointScheduleData(point)

    @property
    def point_map_url(self) -> str:
        return super().point_map_url((self.point.lat, self.point.lon))

    @property
    def notes_lines(self) -> Sequence[str]:
        return [l for l in self.point.notes.splitlines() if l]


class TripData(BaseData[Trip]):
    def name_for(self, user: User):
        if(self._object.author.id == user.id):
            return self._object.name
        else:
            return f"{self._object.author.username}/{self._object.name}"
