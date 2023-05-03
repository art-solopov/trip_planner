from ..models import Trip, Point, User, PrivacyStatusEnum


class Policy:
    def __init__(self, user: User):
        self.user = user

    def is_own_trip(self, trip: Trip):
        return trip.author == self.user

    def can_see_trip(self, trip: Trip):
        return self.is_own_trip(trip) or trip.privacy_status == PrivacyStatusEnum.public

    def trip_points_query(self, trip: Trip):
        # query = trip.points
        query = Point.query.filter_by(trip=trip)
        if trip.author == self.user:
            return query
        else:
            return query.filter_by(privacy_status=PrivacyStatusEnum.public)
