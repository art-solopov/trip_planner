import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory
from passlib.hash import bcrypt
from faker import Faker

from trip_planner import models
from trip_planner.trips.forms import PointForm


from . import db


class UserFactory(Factory):
    class Meta:
        model = models.Trip
        sqlalchemy_session = db.session

    username = factory.Faker('ascii_email')

    @factory.lazy_attribute
    def password_digest(self):
        fake = Faker()
        password = fake.password()
        return bcrypt.hash(password)


class TripFactory(Factory):
    class Meta:
        model = models.Trip
        sqlalchemy_session = db.session

    name = factory.Faker('city')
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(' ', '-'))
    author = factory.SubFactory(UserFactory)


class PointFactory(Factory):
    class Meta:
        model = models.Point
        sqlalchemy_session = db.session

    trip = factory.SubFactory(TripFactory)
    name = factory.Faker('sentence', nb_words=3)
    address = factory.Faker('text')
    lat = factory.Faker('latitude')
    lon = factory.Faker('longitude')
    type = factory.Faker('random_element',
                         elements=[x[0] for x in PointForm.TYPE_CHOICES])
