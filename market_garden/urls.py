from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(r"", include("market_garden.cropmap.urls")),
    path(r"", include("market_garden.daily_chores.urls")),
    path(r"", include("market_garden.mulching.urls")),
    path(r"", include("market_garden.watering.urls")),
    path(r"", include("market_garden.todo.urls")),
]
