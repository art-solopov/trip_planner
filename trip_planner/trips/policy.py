from flask import abort

from .. import db
from ..models import User, Trip, Point


class Policy:
    def __init__(self, user: User):
        self.user = user

    def trips_query(self):
        return db.select(Trip).filter_by(author=self.user)

    def points_query(self, trip: Trip):
        q = Point.query
        if not self.can_see_trip(trip):
            return q.filter(db.false())

        return q.filter(Point.trip == trip)

    def authorize(self, action, *args, **kwargs):
        method = getattr(self, f"can_{action}")
        if not method(*args, **kwargs):
            abort(403, "Unauthorized")

    def can_see_trip(self, trip: Trip):
        return trip.author == self.user

    def can_edit_trip(self, trip: Trip):
        return trip.author == self.user

    def can_delete_trip(self, trip: Trip):
        return self.can_edit_trip(trip)

    def can_add_point(self, trip: Trip):
        return self.can_edit_trip(trip)

    def can_edit_point(self, point: Point):
        return self.can_edit_trip(point.trip)

    def can_delete_point(self, point: Point):
        return self.can_edit_point(point)
