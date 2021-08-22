from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path

schema_view = get_schema_view(
    openapi.Info(
        title="Django Microfarm",
        default_version="v1",
        description="Django Microfarm APIs",
        terms_of_service="",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        r"", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"
    ),
    path(r"docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
