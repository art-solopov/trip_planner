from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password_digest = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Trip(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True,
                          nullable=False)
    name = db.Column(db.String(2000), nullable=False, index=True)
    country_code = db.Column(db.String(2))
    slug = db.Column(db.String(2000), nullable=False)

    author = db.relationship('User',
                             backref=db.backref('trips',
                                                order_by=lambda: Trip.name))

    def __repr__(self):
        return f"<Trip {self.name} [{self.id}] " \
            f"author_id={self.author_id} slug={self.slug}>"


db.Index('idx_trip_author_slug', Trip.author_id, Trip.slug, unique=True)


class Point(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    trip_id = db.Column(db.BigInteger, db.ForeignKey('trip.id'), index=True,
                        nullable=False)
    name = db.Column(db.String(2000), nullable=False, index=True)
    address = db.Column(db.Text)
    lat = db.Column(db.Numeric(8, 5), nullable=False)
    lon = db.Column(db.Numeric(8, 5), nullable=False)
    type = db.Column(db.String(120), nullable=False, index=True)
    notes = db.Column(db.Text)
    schedule = db.Column(db.JSON(none_as_null=True))

    trip = db.relationship('Trip',
                           backref=db.backref(
                               'points',
                               order_by=lambda: (Point.type, Point.name),
                               cascade='save-update, merge, delete'
                           ))
