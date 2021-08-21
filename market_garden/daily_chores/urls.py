from rest_framework.routers import DefaultRouter
from market_garden.daily_chores.views.daily_chores import DailyChoresViewSet

router = DefaultRouter(trailing_slash=True)
router.register(r"api/daily/chores", DailyChoresViewSet, basename="daily_chores")

urlpatterns = router.urls
