from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    password_digest = db.Column(db.String(100), nullable=True)


class Trip(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True,
                          nullable=False)
    name = db.Column(db.String(2000), nullable=False)
    country_code = db.Column(db.String(2))
    slug = db.Column(db.String(2000), nullable=False)

    author = db.relationship('User', backref='trips')


db.Index('idx_trip_author_slug', Trip.author_id, Trip.slug, unique=True)
