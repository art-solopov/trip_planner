class ScheduleClasses:
    WEEKDAYS = {
        '_default': 'bg-black text-white',
        'fri': 'bg-teal-800 text-white',
        'sat': 'bg-orange-300',
        'sun': 'bg-yellow-300'
    }

    CELL_CLASS = 'p-2'
    COMMON_WEEKDAY_CLASS = 'font-bold'


class ViewClasses:
    TRIP_SHOW = 'show-trip flex flex-col md:flex-row md:justify-between'
