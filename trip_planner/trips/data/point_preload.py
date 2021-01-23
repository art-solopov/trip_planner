import re
import urllib.parse as urlp

import requests as rq

GMAPS_LOCATION_RE = re.compile(r'google\.com/maps/place/(?P<name>.*)/' +
                               r'@(?P<lat>\d+\.\d+),(?P<lon>\d+\.\d+),' +
                               r'(?:\d+\w*)/data')


def from_gmaps(url: str) -> dict:
    pre_response = rq.head(url)
    assert pre_response.status_code in range(300, 400)

    new_url = urlp.unquote(pre_response.headers['Location'])
    url_match = re.search(GMAPS_LOCATION_RE, new_url)
    assert url_match

    data = {s: url_match[s] for s in 'name lat lon'.split()}

    return data
