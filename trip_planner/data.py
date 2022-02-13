from flask import current_app


class MapData:
    # MAP_BASE_URL = 'https://api.mapbox.com/styles/v1/mapbox/streets-v11'
    STYLE_KEY = 'art-solopov/ckj1qaoa79v8419szqo9p3dqj'
    MAP_BASE_URL = f'https://api.mapbox.com/styles/v1/{STYLE_KEY}'
    MAPBOX_STYLE_URL = f'mapbox://styles/{STYLE_KEY}'
    ZOOM_LEVEL = 15.5

    @property
    def api_key(self):
        return current_app.config['MAPBOX_APIKEY']

    # @property
    # def map_attribution(self) -> str:
    #     # Taken from Mapbox website
    #     return r'''
# © <a href="https://www.mapbox.com/about/maps/">Mapbox</a>
# © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>
# <strong><a href="https://www.mapbox.com/map-feedback/" target="_blank">
# Improve this map</a></strong>
    #     '''.strip()

    def point_map_url(self, coordinates: (float, float)) -> str:
        lat, lon = coordinates
        width, height = (400, 380)  # TODO: replace with multiple sizes
        return (f"{self.MAP_BASE_URL}/static/pin-l({lon},{lat})/"
                f"{lon},{lat},{self.ZOOM_LEVEL},0,0/"
                f"{width}x{height}"
                f"?access_token={self.api_key}")
