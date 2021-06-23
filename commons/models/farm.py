from django.db import models
from commons.models.base import BaseModel


class FarmModel(BaseModel):
    latitude = models.DecimalField(
        verbose_name="Latitude",
        max_digits=9,
        decimal_places=6,
        editable=True,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        verbose_name="Longitude",
        max_digits=9,
        decimal_places=6,
        editable=True,
        null=True,
        blank=True,
    )
    length = models.DecimalField(
        verbose_name="Length (in meteres)",
        max_digits=9,
        decimal_places=1,
        editable=True,
    )
    width = models.DecimalField(
        verbose_name="Width (in meteres)",
        max_digits=9,
        decimal_places=1,
        editable=True,
    )

    class Meta:
        abstract = True
