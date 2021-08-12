from django.db import models
from commons.models.task import TaskModel
from market_garden.cropmap.models.cropmap import MarketGarden


class DailyChores(TaskModel):
    TIME_CHOICES = (
        (3, "Morning"),
        (2, "Afternoon"),
        (1, "Evening"),
        (0, "Night"),
    )

    is_specific = models.BooleanField(
        verbose_name="Is this a specific market-garden task?",
        default=False,
    )

    market_garden = models.ManyToManyField(
        MarketGarden,
        verbose_name="Market Garden",
        default=None,
        blank=True,
    )

    preferable_time = models.IntegerField(
        verbose_name="Preferable time for task",
        choices=TIME_CHOICES,
    )

    class Meta:
        verbose_name_plural = "04 Daily Chores"

    def __str__(self):
        return self.name
