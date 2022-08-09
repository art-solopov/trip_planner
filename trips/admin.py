from django.contrib import admin
import django.contrib.auth.admin as auth_admin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "email")


class TripLegInline(admin.TabularInline):
    model = models.TripLeg
    ordering = ['position']
    extra = 1


@admin.register(models.Trip)
class TripAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'full_slug', 'author_name')
    list_display_links = ('full_slug',)
    list_select_related = ('author',)

    inlines = [
        TripLegInline
        ]

    @admin.display(description='Author', ordering='author__username')
    def author_name(self, obj: models.Trip):
        return obj.author.username


class TripPointInline(admin.TabularInline):
    model = models.TripPoint


@admin.register(models.TripLeg)
class TripLegAdmin(admin.ModelAdmin):
    list_select_related = ('city', 'trip', 'trip__author')
    list_display = ('trip', 'city', 'position')
    list_display_links = ('city',)
    ordering = ['trip', 'position']

    inlines = [
        TripPointInline
        ]
