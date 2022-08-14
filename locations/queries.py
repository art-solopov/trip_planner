from itertools import groupby
import operator as op

from .models import City, PointOfInterest


class PointsForCity:
    def __call__(self, city: City):
        query = (PointOfInterest.objects.filter(city=city).
                 order_by('type', 'name'))
        groups = {k: list(vals)
                  for k, vals in groupby(query, key=op.attrgetter('type'))}
        choices = PointOfInterest.type.field.choices
        return [(choice, choice_text, groups[choice])
                for choice, choice_text in choices
                if choice in groups]
