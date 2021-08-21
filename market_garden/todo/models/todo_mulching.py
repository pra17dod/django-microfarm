from django.db import models
from rest_framework import serializers
from market_garden.todo.models.todo_status import TodoStatus
from market_garden.mulching.models.mulching_rule import MulchingRule


class TodoMulching(TodoStatus):
    mulching_rule = models.ForeignKey(
        MulchingRule,
        on_delete=models.CASCADE,
        verbose_name="Mulching Rule",
    )

    class Meta:
        verbose_name_plural = "02 Todo Mulching"

    def __str__(self):
        return f"{self.market_garden.user}'s MarketGarden ID-{self.market_garden.id} Todo ID-{self.id}"


class TodoMulchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoMulching
        fields = "__all__"
