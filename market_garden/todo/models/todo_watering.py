from django.db import models
from market_garden.todo.models.todo_status import TodoStatus
from market_garden.watering.models.watering_rule import WateringRule


class TodoWatering(TodoStatus):
    watering_rule = models.ForeignKey(
        WateringRule,
        on_delete=models.CASCADE,
        verbose_name="Watering Rule",
    )

    class Meta:
        verbose_name_plural = "03 Todo Watering"

    def __str__(self):
        return f"{self.market_garden.user}'s MarketGarden ID-{self.market_garden.id} Todo ID-{self.id}"
