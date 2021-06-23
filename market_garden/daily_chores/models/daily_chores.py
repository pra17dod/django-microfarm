from django.db import models
from commons.models.task import TaskModel


class DailyChores(TaskModel):
    TIME_CHOICES = (
        ("morning", "Morning"),
        ("afternoon", "Afternoon"),
        ("evening", "Evening"),
        ("night", "Night"),
    )
    preferable_time = models.CharField(choices=TIME_CHOICES, max_length=15)

    class Meta:
        verbose_name = "Daily Chore"

    def __str__(self):
        return self.name
