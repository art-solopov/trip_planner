from django.conf import settings

from .models import PointOfInterest, GeoPoint


STYLE_KEY = 'art-solopov/ckj1qaoa79v8419szqo9p3dqj'
MAP_BASE_URL = f'https://api.mapbox.com/styles/v1/{STYLE_KEY}'
MAPBOX_STYLE_URL = f'mapbox://styles/{STYLE_KEY}'
ZOOM_LEVEL = 15.5
IMG_WIDTH = 400
IMG_HEIGHT = 300

_api_key = settings.MAPBOX_API_KEY


def static_map_url(point: GeoPoint) -> str:
    width, height = (IMG_WIDTH, IMG_HEIGHT)
    lon = point.lon
    lat = point.lat
    return (f"{MAP_BASE_URL}/static/pin-l({lon},{lat})/"
            f"{lon},{lat},{ZOOM_LEVEL},0,0/"
            f"{width}x{height}"
            f"?access_token={_api_key}")


def point_data(point: PointOfInterest) -> dict:
    return dict(
        name=point.name,
        lat=point.lat,
        lon=point.lon,
        address=point.address,
        slug=point.slug
    )
