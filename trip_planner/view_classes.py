class ScheduleClasses:
    WEEKDAYS = {
        '_default': 'wday-default',
        'fri': 'wday-fri',
        'sat': 'wday-sat',
        'sun': 'wday-sun'
    }

    SCHEDULE_TABLE_CLASS = "schedule-table"
    CELL_CLASS = ''
    HEADER_CELL_CLASS = f"{CELL_CLASS} bold text-center"
    COMMON_WEEKDAY_CLASS = 'weekday bold'
    CONTROL_WEEKDAY_CLASS = 'control'


class ViewClasses:
    TRIP_SHOW = 'show-trip'
    POINT_SHOW = 'show-point'
    AUTH_FORM = 'narrow-form'
