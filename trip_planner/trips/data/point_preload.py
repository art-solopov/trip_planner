import re
import urllib.parse as urlp
from collections import namedtuple
import json

import requests as rq
from bs4 import BeautifulSoup

from trip_planner.trips.forms import PointForm

GMAPS_LOCATION_RE = re.compile(r'google\.com/maps/place/(?P<name>.*)/' +
                               r'@(?P<lat>\d+\.\d+),(?P<lon>\d+\.\d+),' +
                               r'(?:\d+(?:\.\d+)?\w*)/data')
GMAPS_SHORT_LOCATION_RE = re.compile(r'google\.com/maps/place//data')


class PreloaderNotFound(Exception):
    pass


class PreloaderError(Exception):
    pass


Preloader = namedtuple('Preloader', ['re', 'preloader'])


class MakePreload:
    def __init__(self, pattern: str):
        self.re = re.compile(pattern)

    def __call__(self, fn):
        return Preloader(self.re, fn)


def _redirect_reload_location(url: str) -> str:
    rsp = rq.head(url)
    if not 300 <= rsp.status_code < 400:
        raise PreloaderError(f'Expected a redirect, got {rsp.status_code}')

    return urlp.unquote(rsp.headers['Location'])


def _load_data(url: str) -> str:
    response = rq.get(url)
    if response.status_code != 200:
        raise PreloaderError(
            f'Error getting point info: {response.status_code}'
            )
    return response.text


def _load_data_as_soup(url: str) -> BeautifulSoup:
    return BeautifulSoup(_load_data(url))


@MakePreload(r'https://goo.gl/maps')
def from_gmaps_desktop(url: str) -> dict:
    loc_url = _redirect_reload_location(url)

    url_match = re.search(GMAPS_LOCATION_RE, loc_url)
    if url_match is None:
        raise PreloaderError(
            f"Location {loc_url} doesn't match expected structure"
            )

    data = {s: url_match[s] for s in ['lat', 'lon']}

    soup = _load_data_as_soup(loc_url)
    try:
        data.update({
            'name': soup.find('meta', property='og:title')['content'],
            'address': soup.find('meta', property='og:description')['content']
            })
    except TypeError:
        raise PreloaderError('Internal error')

    return data


@MakePreload(r'https://maps.app.goo.gl/')
def from_gmaps_mobile(url: str) -> dict:
    loc_url = _redirect_reload_location(url)

    url_match = re.search(GMAPS_SHORT_LOCATION_RE, loc_url)
    if url_match is None:
        raise PreloaderError(
            f"Location {loc_url} doesn't match expected structure"
            )
    soup = _load_data_as_soup(loc_url)
    try:
        title = soup.find('meta', property='og:title')['content']
        name, address, *_ = title.split('·')
        return {
            'name': name.strip(),
            'address': address.strip()
            }
    except TypeError:
        raise PreloaderError('Internal error')


@MakePreload(r'https://yandex.ru/maps/(-|org)/')
def from_yandex_maps(url: str) -> dict:
    response = rq.get(url)
    if response.status_code != 200:
        raise PreloaderError(
            f'Error getting point info: {response.status_code}'
            )
    soup = BeautifulSoup(response.text)
    try:
        data_script = soup.find('script', class_='config-view',
                                type=re.compile('json$'))
        ya_data = json.loads(data_script.string)
        lon, lat = [float(f) for f in ya_data['query']['poi']['point'].split(',')]
        return {
            'name': soup.find('h1', itemprop='name').text.strip(),
            'address': soup.find('meta', itemprop='address')['content'],
            'lon': lon,
            'lat': lat
            }
    except TypeError:
        raise PreloaderError('Internal error')


PRELOADERS = [
    from_gmaps_desktop, from_gmaps_mobile, from_yandex_maps
]


class PointPreload:
    PARAM_NAME = 'preload_url'

    def __init__(self, url: str, form: PointForm):
        self.url = url
        self.form = form

    def __call__(self) -> dict:
        preloader = self._find_preloader()
        if preloader is None:
            raise PreloaderNotFound

        data = preloader(self.url)
        for k, v in data.items():
            self.form[k].data = v

    def _find_preloader(self):
        for preloader in PRELOADERS:
            if re.match(preloader.re, self.url):
                return preloader.preloader
        return None