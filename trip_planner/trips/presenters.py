from flask import g

from trip_planner.models import Trip, Point, PointTypes


class TripPresenter:
    REGIONAL_INDICATOR_A = 0x1F1E6

    def __init__(self, trip: Trip):
        self.trip = trip

    def belongs_to_current_user(self):
        return self.trip.author == g.user

    def flag(self):
        return ''.join(
            chr(self.REGIONAL_INDICATOR_A + ord(x) - ord('A'))
            for x in self.country_code
        )

    def __getattr__(self, name):
        return getattr(self.trip, name)


class PointPresenter:
    POINT_COLORS = {
        PointTypes.MUSEUM: 'hsl(225, 100%, 60%)',
        PointTypes.SIGHT: 'hsl(194, 71%, 52%)',
        PointTypes.TRANSPORT: 'hsl(130, 67%, 40%)',
        PointTypes.ACCOMODATION: 'hsl(335, 64%, 53%)',
        PointTypes.FOOD: 'hsl(11, 100%, 18%)',
        PointTypes.ENTERTAINMENT: 'hsl(40, 71%, 60%)',
        PointTypes.SHOP: 'hsl(288, 59%, 49%)',
        PointTypes.OTHER: '#aaa'
    }

    @staticmethod
    def point_colors_map():
        return {k.value: v for k, v in PointPresenter.POINT_COLORS.items()}

    @staticmethod
    def point_colors_css():
        return "\n".join(f".is-{k.value} {'{'} --type-color: {v}; {'}'}"
                         for k, v in PointPresenter.POINT_COLORS.items())

    def __init__(self, point: Point):
        self.point = point

    @property
    def type(self):
        return self.point.type.value

    def __getattr__(self, name):
        return getattr(self.point, name)
