from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from locations.models import City, PointOfInterest


class User(AbstractUser):
    # Removing first_name and last_name. Everything else
    # can stay
    first_name = None
    last_name = None


class Trip(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=600)

    class Meta:
        constraints = [
            models.UniqueConstraint('author', 'slug',
                                    name='trip_unique_author_slug')
            ]
        indexes = [
            models.Index(fields=['author', 'name']),
            models.Index(fields=['author', 'slug'])
            ]


class TripLeg(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    position = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint('trip', 'position',
                                    name='trip_leg_unique_trip_position')
            ]
        indexes = [
            models.Index(fields=['trip', 'position'])
            ]


class TripPoint(models.Model):
    trip_leg = models.ForeignKey(TripLeg, on_delete=models.CASCADE)
    poi = models.ForeignKey(PointOfInterest, on_delete=models.CASCADE)
    # TODO: add validation that poi belongs to the same city as trip leg
