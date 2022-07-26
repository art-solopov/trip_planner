import django.views.generic as v

from .models import City, PointOfInterest


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
        context['points'] = self._get_points()
        return context

    def _get_points(self):
        city = self.get_object()
        return city.pointofinterest_set.order_by('type', 'name')


class PointOfInterestDetail(v.DetailView):
    model = PointOfInterest
    context_object_name = 'point'
    template_name = 'locations/point_detail.html'
