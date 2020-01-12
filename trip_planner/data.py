from flask import current_app


class MapData:
    MAP_BASE_URL = 'https://api.mapbox.com/styles/v1/mapbox/streets-v11'
    ZOOM_LEVEL = 15.5

    @property
    def api_key(self):
        return current_app.config['MAPBOX_APIKEY']

    @property
    def map_url(self) -> str:
        return (f"{self.MAP_BASE_URL}/tiles/256/{{z}}/{{x}}/{{y}}"
                f"?access_token={self.api_key}")

    def point_map_url(self, coordinates: (float, float)) -> str:
        lat, lon = coordinates
        width, height = (400, 380)  # TODO: replace with multiple sizes
        return (f"{self.MAP_BASE_URL}/static/pin-l({lon},{lat})/"
                f"{lon},{lat},{self.ZOOM_LEVEL},0,0/"
                f"{width}x{height}"
                f"?access_token={self.api_key}")
