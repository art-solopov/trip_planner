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
    LOGIN_FORM = 'mx-auto w-72'


class FlashClasses:
    ALL = 'rounded-md p-3 mb-1 border flex justify-between'
    CATEGORIES = {
        'error': 'border-red-700 bg-red-100',
        'success': 'border-green-700 bg-green-100'
    }


class CommonClasses:
    TITLE_H1 = 'mb-4 text-2xl'
    TITLE_H1_BIG = 'mb-4 text-3xl'
    NAVBAR_TEXT = 'mx-2 whitespace-nowrap'
    NAVBAR_LINK = NAVBAR_TEXT + ' btn btn-light-2 btn-small'


class FormClasses:
    INPUT_DEFAULT = 'w-full'
