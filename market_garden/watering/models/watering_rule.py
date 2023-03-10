from django.db import models
from rest_framework import serializers
from django.conf import settings
from commons.models.base import BaseModel
from commons.models.rule import RuleModel
from market_garden.cropmap.models.cropmap import MarketGarden
from market_garden.watering.scripts.watering import WateringRequired
from autoslug import AutoSlugField


class WateringRule(BaseModel):
    market_garden = models.ForeignKey(
        MarketGarden, on_delete=models.CASCADE, verbose_name="Market Garden"
    )
    slug = AutoSlugField(
        verbose_name="Slug",
        populate_from="market_garden",
        max_length=50,
        editable=True,
        blank=True,
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
        default=False,
        editable=True,
    )
    last_watered_at = models.DateTimeField(
        verbose_name="Last Watered at",
    )
    lower_temp = models.DecimalField(
        verbose_name="Lower Temp. under which watering not required (in deg. C)",
        max_digits=4,
        decimal_places=1,
        default=4.0,
        editable=True,
        blank=True,
    )
    max_hours_for_next_rain = models.IntegerField(
        verbose_name="Max Hours to check Forecast for Rain",
        editable=True,
        default=5,
        blank=True,
    )
    min_hours_gap_btw_watering = models.IntegerField(
        verbose_name="Max Hours between Watering",
        editable=True,
        default=19,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "06 Watering Rules"

    def __str__(self):
        return f"{self.market_garden.user} - Market Garden ID-{self.market_garden.id}"

    def watering_rule(self):
        return WateringRequired(
            self.start_week,
            self.end_week,
            self.if_rain,
            self.last_watered_at,
            self.lower_temp,
            self.max_hours_for_next_rain,
            self.min_hours_gap_btw_watering,
            self.market_garden.latitude,
            self.market_garden.longitude,
            self.market_garden.timezone,
        )

    def todo_watering(self):
        return self.watering_rule().watering_required()

    def is_raining(self):
        value, curr_temp = self.watering_rule().weather_now()
        return value


class WateringRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WateringRule
        fields = "__all__"
