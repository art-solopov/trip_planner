import calendar

from django import template
from ..models import PointOfInterest

register = template.Library()


@register.inclusion_tag('locations/_schedule.html')
def render_schedule(point: PointOfInterest):
    weekdays = [wd.lower() for wd in calendar.day_abbr]
    point_schedule = point.schedule or dict()
    schedule = [(wd, point_schedule.get(wd)) for wd in weekdays]
    return {'schedule': schedule}
