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
    TRIP_SHOW = ' '.join(['show-trip flex flex-col',
                          'lg:flex-row lg:justify-between',
                          'lg:max-h-body-sans-header'])


class FlashClasses:
    ALL = 'rounded-md p-3 mb-1 border'
    CATEGORIES = {
        'error': 'border-red-700 bg-red-100',
        'success': 'border-green-700 bg-green-100'
    }