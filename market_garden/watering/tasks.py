from __future__ import absolute_import, unicode_literals

from celery import shared_task
from market_garden.watering.models.watering_rule import WateringRule
from django.utils import timezone
from django.shortcuts import get_object_or_404


@shared_task
def hourly_weather_check():
    objects = WateringRule.objects.all()
    for obj in objects:
        if obj.is_raining():
            obj.last_watered_at = timezone.now()


@shared_task
def check_watering_required(*args, **kwargs):
    instance_id = args[0]
    instance = get_object_or_404(WateringRule, id=instance_id)
    value, reason = instance.todo_watering()
    if value:
        return f"{reason}! Watering is required for your market-garden!!"
    else:
        return f"{reason}! Watering is not required for your market-garden!! Enjoy your time!"
