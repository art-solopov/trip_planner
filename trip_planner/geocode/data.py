from dataclasses import dataclass
from typing import List
from logging import getLogger, DEBUG

from flask import current_app
from requests import get
from box import Box

from ..data import MapData
from ..models import Trip
from .forms import GeocodeForm

GEOCODE_ENDPOINT = 'https://nominatim.openstreetmap.org/search'


logger = getLogger('trip_planner.geocode')


@dataclass
class PointData:
    lat: float
    lon: float
    address: str
    name: str
    map_url: str


def _point_data(map_data: MapData, response_item: dict) -> PointData:
    ri_box = Box(response_item, default_box=True)
    lat = float(ri_box.lat)
    lon = float(ri_box.lon)
    address = ri_box.display_name
    name = ri_box.namedetails.setdefault('name', address.split(', ')[0])
    return PointData(lat=lat, lon=lon, address=address,
                     name=name, map_url=map_data.point_map_url((lat, lon)))


def geocode(form: GeocodeForm, country_code: str = None) -> List[PointData]:
    if form.geocode_field.data == 'address':
        search = form.address.data
    else:
        search = form.name.data

    map_data = MapData()
    response = get(GEOCODE_ENDPOINT,
                   params={'format': 'json', 'q': search,
                           'countrycodes': country_code, 'namedetails': 1},
                   headers={'user-agent': 'trip-planner.geocode/1.0'})
    logger.info('Sending geocoding request to %s', response.request.url)
    logger.debug('Received geocoding response with status=%d, body=%s',
                 response.status_code, (response.text if response.status_code > 400 else '...'))
    return [_point_data(map_data, x) for x in response.json()]
