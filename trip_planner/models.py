import enum
from secrets import token_urlsafe

from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import ARRAY

from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password_digest = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<User {self.username} [{self.id}]>"


class Trip(db.Model):
    @staticmethod
    def generate_key():
        return token_urlsafe(10)

    id = db.Column(db.BigInteger, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True,
                          nullable=False)
    name = db.Column(db.String(2000), nullable=False, index=True)
    country_code = db.Column(db.String(2))
    author = db.relationship('User',
                             backref=db.backref('trips',
                                                order_by=lambda: Trip.name))
    center_lat = db.Column(db.Numeric(8, 5), nullable=True)
    center_lon = db.Column(db.Numeric(8, 5), nullable=True)
    key = db.Column(db.String(200), nullable=True, index=True, default=generate_key, unique=True)

    def __repr__(self):
        return f"<Trip {self.name} [{self.id}] " \
            f"author_id={self.author_id} key={self.key}>"


class PointTypes(enum.Enum):
    MUSEUM = 'museum'
    SIGHT = 'sight'
    TRANSPORT = 'transport'
    ACCOMODATION = 'accomodation'
    FOOD = 'food'
    ENTERTAINMENT = 'entertainment'
    SHOP = 'shop'
    OTHER = 'other'


class Point(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    trip_id = db.Column(db.BigInteger, db.ForeignKey('trip.id'), index=True,
                        nullable=False)
    name = db.Column(db.String(2000), nullable=False, index=True)
    address = db.Column(db.Text)
    lat = db.Column(db.Numeric(8, 5), nullable=False)
    lon = db.Column(db.Numeric(8, 5), nullable=False)
    type = db.Column(db.Enum(PointTypes,
                             native_enum=False,
                             length=120,
                             values_callable=lambda x: [i.value for i in x]),
                     nullable=False, index=True)
    notes = db.Column(db.Text)
    schedule = db.Column(db.JSON(none_as_null=True))
    websites = db.Column(ARRAY(db.String(2000)), nullable=True)

    trip = db.relationship('Trip',
                           backref=db.backref(
                               'points',
                               order_by=lambda: (Point.type, Point.name),
                               cascade='save-update, merge, delete'
                           ))

    @validates('websites')
    def delete_empty_websites(self, _key, websites):
        return [x for x in websites if x]
