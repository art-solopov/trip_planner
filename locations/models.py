from django.db import models
from django_countries.fields import CountryField


class GeoPoint(models.Model):
    lat = models.DecimalField(verbose_name="latitude",
                              max_digits=8, decimal_places=5)
    lon = models.DecimalField(verbose_name="longitude",
                              max_digits=8, decimal_places=5)

    class Meta:
        abstract = True


class CityManager(models.Manager):
    def available_for_view(self):
        points_subq = PointOfInterest.objects.filter(
            city=models.OuterRef('pk'))
        return self.filter(models.Exists(points_subq))


class City(GeoPoint, models.Model):
    name = models.CharField(max_length=500, db_index=True)
    country = CountryField()
    slug = models.SlugField(max_length=500, unique=True)

    objects = CityManager()

    def __str__(self):
        return f'{self.name} {self.country.code}'

    class Meta:
        verbose_name_plural = 'cities'


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
    address = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=500)
    type = models.CharField(max_length=255, choices=POINT_TYPES)
    schedule = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['city', 'name']),
            models.Index(fields=['city', 'slug'])
            ]
        verbose_name_plural = 'points of interest'
