from itertools import groupby
import operator as op

from .models import City, PointOfInterest


class PointsForCity:
    def __call__(self, city: City):
        return [(k, list(vals)) for (k, vals) in groupby(
            PointOfInterest.objects.filter(city=city).order_by('type', 'name'),
            key=op.attrgetter('type')
            )]
