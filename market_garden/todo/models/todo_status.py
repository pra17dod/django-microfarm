from django.db import models
from commons.models.base import BaseModel
from market_garden.cropmap.models.cropmap import MarketGarden


class TodoStatus(BaseModel):
    TASK_STATUS = (
        (3, "Upcoming"),
        (2, "Started"),
        (1, "Paused"),
        (0, "Completed"),
        (-1, "Over Dued"),
    )

    market_garden = models.ForeignKey(
        MarketGarden,
        on_delete=models.CASCADE,
        verbose_name="Market Garden",
    )

    status = models.IntegerField(
        verbose_name="Task's status",
        choices=TASK_STATUS,
        default=3,
    )

    class Meta:
        abstract = True
