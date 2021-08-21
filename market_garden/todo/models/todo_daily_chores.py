from django.db import models
from rest_framework import serializers
from market_garden.todo.models.todo_status import TodoStatus
from market_garden.daily_chores.models.daily_chores import DailyChores


class TodoDailyChores(TodoStatus):
    daily_chores = models.ForeignKey(
        DailyChores,
        on_delete=models.CASCADE,
        verbose_name="Daily Chores",
    )

    class Meta:
        verbose_name_plural = "01 Todo Daily Chores"

    def __str__(self):
        return f"{self.market_garden.user}'s MarketGarden ID-{self.market_garden.id} Todo ID-{self.id}"


class TodoDailyChoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoDailyChores
        fields = "__all__"
