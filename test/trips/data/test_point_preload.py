import unittest.mock as mock

import requests
import pytest as pt
import pytest_mock

from trip_planner.trips.data.point_preload import (
    PreloaderError,
    from_gmaps_desktop, from_gmaps_mobile, from_yandex_maps
    )


def test_re_match() -> None:
    assert from_gmaps_desktop.re.match('https://example.com') is None


client_error_response = mock.Mock(requests.Response, status_code=401)


def _redirect_response(location: str = 'https://r.example.com') -> mock.Mock:
    return mock.Mock(
        requests.Response,
        status_code=302, headers={'Location': location}
        )


success_html = '''
<html>
    <head>
    <meta property="og:title" content="Title · T2">
    <meta property="og:description" content="Description">
    <meta itemprop="address" content="Address">
    </head>
    <body>
        <h1 itemprop="name">Title</h1>
        <script class="config-view" type="application/json">
        {
            "query": {
                "mode": "poi",
                "poi": {
                    "point": "51.5,0.1"
                }
            },
            "mapLocation": {
                "center": [51.55, 0.25]
            }
        }
        </script>
    </body>
</html>
'''

success_response = mock.Mock(requests.Response,
                             status_code=200, text=success_html.strip())


def test_google_maps_not_redirect(mocker: pytest_mock.MockerFixture) -> None:
    mocker.patch('requests.head', return_value=client_error_response)
    with pt.raises(PreloaderError):
        from_gmaps_desktop.preloader('https://example.com')
    requests.head.assert_called()


def test_google_maps_success(mocker: pytest_mock.MockerFixture) -> None:
    redirect_url = 'https://google.com/maps/place/Name/@51.50,0.1,14z/data'
    mocker.patch('requests.head',
                 return_value=_redirect_response(redirect_url))
    mocker.patch('requests.get', return_value=success_response)
    assert from_gmaps_desktop.preloader('https://example.com') == {
        'name': "Title · T2",
        'address': "Description",
        'lat': '51.50',
        'lon': '0.1'
    }
    requests.head.assert_called()
    requests.get.assert_called_with(redirect_url)


def test_mobile_gmaps_not_redirect(mocker: pytest_mock.MockerFixture) -> None:
    mocker.patch('requests.head', return_value=client_error_response)
    with pt.raises(PreloaderError):
        from_gmaps_mobile.preloader('https://example.com')
    requests.head.assert_called()


def test_mobile_gmaps_success(mocker: pytest_mock.MockerFixture) -> None:
    redirect_url = 'https://google.com/maps/place//data'
    mocker.patch('requests.head',
                 return_value=_redirect_response(redirect_url))
    mocker.patch('requests.get', return_value=success_response)
    assert from_gmaps_mobile.preloader('https://example.com') == {
        'name': "Title",
        'address': 'T2'
    }


def test_yandex_maps_success(mocker: pytest_mock.MockerFixture) -> None:
    mocker.patch('requests.get', return_value=success_response)
    assert from_yandex_maps.preloader('https://example.com') == {
        'name': "Title",
        'address': "Address",
        'lon': 51.50,
        'lat': 0.1
    }
