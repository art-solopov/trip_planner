from flask import Blueprint, request
from flask.json import jsonify
from requests import get
from box import Box

from .. import csrf
from ..shared import user_requred
from ..data import MapData


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


def _geocode(search, country_code):
    map_data = MapData()
    response = get(GEOCODE_ENDPOINT, params={'format': 'json',
                                             'q': search,
                                             'countrycodes': country_code,
                                             'namedetails': 1})
    return [_point_data(map_data, x) for x in response.json()]


@api.route("/geocode", methods=('POST',))
@csrf.exempt
@user_requred
def api_geocode():
    search = request.json['search']
    country_code = request.json.get('country_code', '')
    return jsonify(_geocode(search, country_code))
