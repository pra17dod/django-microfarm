from rest_framework.routers import DefaultRouter
from market_garden.mulching.views.mulching_rule import (
    MulchingRuleViewSet,
    CustomMulchingRuleViewSet,
)

router = DefaultRouter(trailing_slash=True)
router.register(r"api/rule/mulching", MulchingRuleViewSet, basename="mulching_rule")
router.register(
    r"api/rule/mulching/custom",
    CustomMulchingRuleViewSet,
    basename="custom_mulching_rule",
)

urlpatterns = router.urls
