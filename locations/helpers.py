from django.conf import settings


class MapData:
    STYLE_KEY = 'art-solopov/ckj1qaoa79v8419szqo9p3dqj'
    MAP_BASE_URL = f'https://api.mapbox.com/styles/v1/{STYLE_KEY}'
    MAPBOX_STYLE_URL = f'mapbox://styles/{STYLE_KEY}'
    ZOOM_LEVEL = 15.5
    IMG_WIDTH = 400
    IMG_HEIGHT = 300

    @property
    def api_key(self):
        return settings.MAPBOX_API_KEY

    def static_map_url(self, lat, lon) -> str:
        width, height = (400, 300)  # TODO: replace with other sizes
        return (f"{self.MAP_BASE_URL}/static/pin-l({lon},{lat})/"
                f"{lon},{lat},{self.ZOOM_LEVEL},0,0/"
                f"{width}x{height}"
                f"?access_token={self.api_key}")
