from flask import Blueprint, request, current_app
from flask.json import jsonify
from requests import get
from box import Box
from werkzeug.datastructures import MultiDict

from .. import csrf
from ..shared import user_required
from ..models import Trip
from ..data import MapData
from .forms import GeocodeForm


api = Blueprint('api', __name__, url_prefix='/api')


GEOCODE_ENDPOINT = 'https://nominatim.openstreetmap.org/search'


def _point_data(map_data: MapData, response_item: dict) -> dict:
    ri_box = Box(response_item, default_box=True)
    lat = float(ri_box.lat)
    lon = float(ri_box.lon)
    address = ri_box.display_name
    name = ri_box.namedetails.setdefault('name', address.split(', ')[0])
    return {
        'lat': lat,
        'lon': lon,
        'address': address,
        'name': name,
        'map_url': map_data.point_map_url((lat, lon))
    }


def _geocode(form: GeocodeForm, trip_id):
    if form.field.data == 'address':
        search = form.address.data
    else:
        search = form.name.data

    map_data = MapData()
    trip = Trip.query.get_or_404(trip_id)
    if trip.name not in search:
        search = f"{search}, {trip.name}"
    response = get(GEOCODE_ENDPOINT, params={'format': 'json',
                                             'q': search,
                                             'countrycodes': trip.country_code,
                                             'namedetails': 1})
    current_app.logger.info((response.request.url, response.request.body))
    return [_point_data(map_data, x) for x in response.json()]


@api.route("/geocode", methods=('POST',))
@csrf.exempt
@user_required
def api_geocode():
    form = GeocodeForm(MultiDict(request.json))
    trip_id = request.json['trip_id']
    return jsonify(_geocode(form, trip_id))
