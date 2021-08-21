from rest_framework.routers import DefaultRouter
from market_garden.watering.views.watering_rule import WateringRuleViewSet

router = DefaultRouter(trailing_slash=True)
router.register(r"api/rule/watering", WateringRuleViewSet, basename="watering_rule")

urlpatterns = router.urls
