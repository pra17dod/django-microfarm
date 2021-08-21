from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(r"auth/", include("microfarm.auth_urls")),
    path(r"", include("market_garden.urls")),
]
