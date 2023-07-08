from flask import g

from trip_planner.models import Trip


class TripPresenter:
    def __init__(self, trip: Trip):
        self.trip = trip

    def belongs_to_current_user(self):
        return self.trip.author == g.user

    def __getattr__(self, name):
        return getattr(self.trip, name)
