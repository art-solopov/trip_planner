from django.db import models
from django.conf import settings
from django_countries.fields import CountryField


class GeoPoint(models.Model):
    lat = models.DecimalField(verbose_name="latitude",
                              max_digits=8, decimal_places=5)
    lon = models.DecimalField(verbose_name="longitude",
                              max_digits=8, decimal_places=5)

    class Meta:
        abstract = True


class City(GeoPoint, models.Model):
    name = models.CharField(max_length=500, db_index=True)
    country = CountryField()
    slug = models.SlugField(max_length=500, unique=True)


class PointOfInterest(GeoPoint, models.Model):
    POINT_TYPES = [
        ('museum', 'Museum'),
        ('sight', 'Sight'),
        ('entertainment', 'Entertainment'),
        ('food', 'Food'),
        ('accomodation', 'Accomodation'),
        ('transport', 'Transport'),
        ('shop', 'Shop'),
        ('other', 'Other'),
        ]

    city = models.ForeignKey(City, on_delete=models.PROTECT)
    name = models.CharField(max_length=500)
    address = models.TextField()
    notes = models.TextField()
    slug = models.SlugField(max_length=500)
    type = models.CharField(max_length=255, choices=POINT_TYPES)
    schedule = models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['city', 'name']),
            models.Index(fields=['city', 'slug'])
            ]


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
