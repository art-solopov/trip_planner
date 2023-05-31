class ScheduleClasses:
    WEEKDAYS = {
        '_default': 'wday-default',
        'fri': 'wday-fri',
        'sat': 'wday-sat',
        'sun': 'wday-sun'
    }

    CELL_CLASS = 'p-2'
    HEADER_CELL_CLASS = f"{CELL_CLASS} fw-bold text-center"
    COMMON_WEEKDAY_CLASS = 'fw-bold'


class ViewClasses:
    TRIP_SHOW = 'show-trip'
    POINT_SHOW = 'show-point'
    LOGIN_FORM = 'login-form mx-auto'
