from flask import g

from trip_planner.models import Trip, Point, PointTypes


class TripPresenter:
    def __init__(self, trip: Trip):
        self.trip = trip

    def belongs_to_current_user(self):
        return self.trip.author == g.user

    def __getattr__(self, name):
        return getattr(self.trip, name)


class PointPresenter:
    POINT_COLORS = {
        PointTypes.MUSEUM: '#be3e66',
        PointTypes.SIGHT: '#5c0d74',
        PointTypes.TRANSPORT: '#5b6b34',
        PointTypes.ACCOMODATION: '#eba92b',
        PointTypes.FOOD: '#65b0aa',
        PointTypes.ENTERTAINMENT: '#a284a0',
        PointTypes.SHOP: '#982c24',
        PointTypes.OTHER: '#aaa'
    }

    @staticmethod
    def point_colors_map():
        return {k.value: v for k, v in PointPresenter.POINT_COLORS.items()}

    def __init__(self, point: Point):
        self.point = point

    @property
    def type(self):
        return self.point.type.value

    def __getattr__(self, name):
        return getattr(self.point, name)
