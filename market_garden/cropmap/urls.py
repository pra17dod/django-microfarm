from django.urls import path, include
from rest_framework.routers import DefaultRouter
from market_garden.cropmap.views.cropmap import (
    MarketGardenViewSet,
    SectionListView,
    SectionDetailView,
    BedListView,
    BedDetailView,
)

router = DefaultRouter(trailing_slash=True)
router.register(r"api/market/garden", MarketGardenViewSet, basename="market_garden")

urlpatterns = [
    path(
        r"api/market/garden/<int:pk_mk>/section/",
        SectionListView.as_view(),
        name="market_garden-section-list",
    ),
    path(
        r"api/market/garden/<int:pk_mk>/section/<int:pk>/",
        SectionDetailView.as_view(),
        name="market_garden-section-detail",
    ),
    path(
        r"api/market/garden/<int:pk_mk>/section/<int:pk_sec>/bed/",
        BedListView.as_view(),
        name="market_garden-section-bed-list",
    ),
    path(
        r"api/market/garden/<int:pk_mk>/section/<int:pk_sec>/bed/<int:pk>/",
        BedDetailView.as_view(),
        name="market_garden-section-bed-detail",
    ),
]

urlpatterns += router.urls
