from rest_framework import viewsets
from market_garden.daily_chores.permissions import IsSpecific
from market_garden.daily_chores.models.daily_chores import (
    DailyChores,
    DailyChoresSerializer,
)


class DailyChoresViewSet(viewsets.ModelViewSet):
    queryset = DailyChores.objects.all()
    serializer_class = DailyChoresSerializer
    permission_classes = [IsSpecific]
