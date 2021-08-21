from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from commons.scripts.get_user_id import get_user_id
from commons.permissions import IsMarketGardenOwner
from market_garden.watering.models.watering_rule import (
    WateringRule,
    WateringRuleSerializer,
)


class WateringRuleViewSet(viewsets.ModelViewSet):
    queryset = WateringRule.objects.all()
    serializer_class = WateringRuleSerializer
    permission_classes = [IsMarketGardenOwner]

    def get_queryset(self, **kwargs):
        """
        This view should return a list of all watering rules for the
        currently authenticated user's market-garden.
        """
        data = get_user_id(self.request)
        objects = WateringRule.objects.all().select_related("market_garden")
        rules = objects.filter(market_garden__user_id=data["user_id"])
        if rules:
            return rules
        else:
            raise NotFound
