from flask import g

from trip_planner.models import Trip, Point


class TripPresenter:
    def __init__(self, trip: Trip):
        self.trip = trip

    def belongs_to_current_user(self):
        return self.trip.author == g.user

    def __getattr__(self, name):
        return getattr(self.trip, name)


class PointPresenter:
    def __init__(self, point: Point):
        self.point = point

    @property
    def type(self):
        return self.point.type.value

    def __getattr__(self, name):
        return getattr(self.point, name)
