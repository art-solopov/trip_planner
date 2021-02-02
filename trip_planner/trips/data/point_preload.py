import re
import urllib.parse as urlp
from collections import namedtuple

import requests as rq
from bs4 import BeautifulSoup

from trip_planner.trips.forms import PointForm

GMAPS_LOCATION_RE = re.compile(r'google\.com/maps/place/(?P<name>.*)/' +
                               r'@(?P<lat>\d+\.\d+),(?P<lon>\d+\.\d+),' +
                               r'(?:\d+(?:\.\d+)?\w*)/data')


class PreloaderNotFound(Exception):
    pass


class PreloaderError(Exception):
    pass


def from_gmaps(url: str) -> dict:
    pre_response = rq.head(url)
    if not 300 <= pre_response.status_code < 400:
        raise PreloaderError(
            f'Expected a redirect, got {pre_response.status_code}'
            )

    new_url = urlp.unquote(pre_response.headers['Location'])
    print(new_url)
    url_match = re.search(GMAPS_LOCATION_RE, new_url)
    if url_match is None:
        raise PreloaderError(
            f"Location {new_url} doesn't match expected structure"
            )

    data = {s: url_match[s] for s in ['lat', 'lon']}

    main_response = rq.get(new_url)
    if main_response.status_code != 200:
        raise PreloaderError(
            f'Error getting point info: {main_response.status_code}'
            )

    soup = BeautifulSoup(main_response.text)
    data.update({
        'name': soup.find('meta', property='og:title')['content'],
        'address': soup.find('meta', property='og:description')['content']
    })

    return data


Preloader = namedtuple('Preloader', ['re', 'preloader'])

PRELOADERS = [
    Preloader(re.compile(r'https://goo.gl/maps'), from_gmaps)
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
