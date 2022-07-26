"""trip_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .home_views import home
from locations import views as locations_views

urlpatterns = [
    path('', home),
    path('cities', locations_views.CitiesList.as_view(), name="cities-list"),
    path('cities/<str:country>/<slug:slug>', locations_views.CityDetail.as_view(), name="city-detail"),
    path('points/<int:pk>', locations_views.PointOfInterestDetail.as_view(), name='point-detail'),
    path('admin/', admin.site.urls),
]
