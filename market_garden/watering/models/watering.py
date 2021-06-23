from django.db import models
from django.conf import settings
from commons.models.base import BaseModel
from commons.models.rule import RuleModel
from market_garden.cropmap.models.section import Section
from autoslug import AutoSlugField


class WateringRule(BaseModel):
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
    )
    slug = AutoSlugField(
        verbose_name="Slug",
        populate_from="name",
        max_length=50,
        editable=True,
    )
    start_week = models.IntegerField(
        verbose_name="Start Week",
        editable=True,
        blank=True,
        null=True,
    )
    end_week = models.IntegerField(
        verbose_name="End Week",
        editable=True,
        blank=True,
        null=True,
    )
    if_rain = models.BooleanField(
        verbose_name="If Rain then watering?",
        default=True,
        editable=True,
    )
    last_watered_at = models.DateTimeField(
        verbose_name="Last Watered at",
    )
    lower_temp = models.DecimalField(
        verbose_name="Lower Temp. under which watering not required",
        max_digits=4,
        decimal_places=1,
        default=4.0,
        editable=True,
        blank=True,
    )
    upper_temp = models.DecimalField(
        verbose_name="Upper Temp. under which watering required",
        max_digits=4,
        decimal_places=1,
        default=15.0,
        editable=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.section.user} - {self.section.name}"


class CustomWateringRule(RuleModel):
    parent_rule = models.ForeignKey(
        WateringRule,
        verbose_name="Custom Rule",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.parent_rule.name} - {self.name}"
