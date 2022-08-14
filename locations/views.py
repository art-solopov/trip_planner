import itertools as it

import django.views.generic as v

import trip_planner.home_views as hv
from .models import City, PointOfInterest
from . import queries as q, map_data


class CitiesList(v.ListView):
    model = City
    queryset = City.objects.available_for_view().order_by('country', 'name')


class CityDetail(v.DetailView):
    model = City

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(country=self.kwargs['country'].upper())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        points = self._get_points()
        context['grouped_points'] = points
        context['flat_points'] = [map_data.point_data(pt)
                                  for pt in it.chain(*(l for _, _, l in points))]
        return context

    def _get_points(self):
        city = self.get_object()
        query = q.PointsForCity()
        return query(city)


class PointOfInterestDetail(hv.WithMainClassMixin, v.DetailView):
    model = PointOfInterest
    context_object_name = 'point'
    template_name = 'locations/point_detail.html'
    main_class = 'point-detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        point = self.get_object()
        map_data = helpers.MapData()
        context['map_url'] = map_data.static_map_url(point.lat, point.lon)
        context['map_height'] = map_data.IMG_HEIGHT
        context['map_width'] = map_data.IMG_WIDTH
        return context
