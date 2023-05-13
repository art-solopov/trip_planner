import factory
from factory.alchemy import SQLAlchemyModelFactory as Factory
from passlib.hash import bcrypt
from faker import Faker

from trip_planner import models
from trip_planner.trips.forms import PointForm
from trip_planner import db


class FactoryMeta:
    sqlalchemy_session = db.session


class UserFactory(Factory):
    class Meta(FactoryMeta):
        model = models.User

    username = factory.Faker('ascii_email')

    @factory.lazy_attribute
    def password_digest(self):
        fake = Faker()
        password = fake.password()
        return bcrypt.hash(password)


class TripFactory(Factory):
    class Meta(FactoryMeta):
        model = models.Trip

    name = factory.Faker('city')
    slug = factory.LazyAttribute(lambda o: o.name.lower().replace(' ', '-'))
    author = factory.SubFactory(UserFactory)
    privacy_status = 'private'

    @factory.post_generation
    def points_count(obj, create, extracted):
        if extracted is None or int(extracted) == 0:
            return

        extracted = int(extracted)

        PointFactory.generate_batch(
            'create' if create else 'build',
            extracted,
            trip=obj
            )


class PointFactory(Factory):
    class Meta(FactoryMeta):
        model = models.Point

    trip = factory.SubFactory(TripFactory)
    name = factory.Faker('sentence', nb_words=3)
    address = factory.Faker('text')
    lat = factory.Faker('latitude')
    lon = factory.Faker('longitude')
    type = factory.Faker('random_element',
                         elements=[x[0] for x in PointForm.TYPE_CHOICES])
    privacy_status = 'private'
