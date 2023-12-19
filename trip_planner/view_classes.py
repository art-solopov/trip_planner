class ScheduleClasses:
    WEEKDAYS = {
        '_default': 'wday-default',
        'fri': 'wday-fri',
        'sat': 'wday-sat',
        'sun': 'wday-sun'
    }

    CELL_CLASS = ''
    HEADER_CELL_CLASS = f"{CELL_CLASS} pm-text-center"
    COMMON_WEEKDAY_CLASS = 'fw-bold'


class ViewClasses:
    TRIP_SHOW = 'show-trip'
    POINT_SHOW = 'plume show-point'
    AUTH_FORM = 'narrow-form'
