from django.contrib import admin

import django.utils.html as h

from .models import City, PointOfInterest


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_display')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Country', ordering='country')
    def country_display(self, obj: City):
        return h.format_html('<img title="{}" src="{}">',
                             obj.country.name, obj.country.flag)


@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'city_name', 'city_country')
    list_select_related = ('city',)
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='City', ordering='city__name')
    def city_name(self, obj):
        return obj.city.name

    @admin.display(description='Country', ordering='city__country')
    def city_country(self, obj):
        return h.format_html('<img title="{}" src="{}">',
                             obj.city.country.name, obj.city.country.flag)
