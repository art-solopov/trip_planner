from flask import current_app


class TripsData:
    MAP_BASE_URL = ('https://api.mapbox.com/styles/v1/mapbox/' +
                    'streets-v11/tiles/256/{z}/{x}/{y}')

    @property
    def map_url(self):
        api_key = current_app.config['MAPBOX_APIKEY']
        return f"{self.MAP_BASE_URL}?access_token={api_key}"
