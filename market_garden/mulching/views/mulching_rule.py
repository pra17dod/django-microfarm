from rest_framework import viewsets
from market_garden.mulching.permissions import SafeOnly
from commons.permissions import IsOwner
from commons.scripts.get_user_id import get_user_id
from market_garden.mulching.models.mulching_rule import (
    MulchingRule,
    CustomMulchingRule,
    MulchingRuleSerializer,
    CustomMulchingRuleSerializer,
)


class MulchingRuleViewSet(viewsets.ModelViewSet):
    queryset = MulchingRule.objects.all()
    serializer_class = MulchingRuleSerializer
    permission_classes = [SafeOnly]


class CustomMulchingRuleViewSet(viewsets.ModelViewSet):
    queryset = CustomMulchingRule.objects.all()
    serializer_class = CustomMulchingRuleSerializer
    permission_classes = [IsOwner]

    def get_queryset(self, **kwargs):
        """
        This view should return a list of all custom mulching rules for the
        currently authenticated user's market-garden.
        """
        data = get_user_id(request)
        rules = CustomMulchingRule.objects.filter(user_id=data["user_id"])
        if rules:
            return rules
        else:
            raise NotFound
