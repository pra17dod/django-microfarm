from __future__ import absolute_import, unicode_literals

from celery import shared_task
from commons.scripts.time import is_current_week_in_range
from market_garden.daily_chores.models.daily_chores import DailyChores
from market_garden.mulching.models.mulching_rule import MulchingRule
from market_garden.watering.models.watering_rule import WateringRule
from market_garden.todo.models.todo_daily_chores import TodoDailyChores
from market_garden.todo.models.todo_mulching import TodoMulching
from market_garden.todo.models.todo_watering import TodoWatering
from market_garden.cropmap.models.cropmap import MarketGarden
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q


@shared_task
def create_todo_daily_chores(*args, **kwargs):
    instance_id = args[0]
    instance = get_object_or_404(MarketGarden, id=instance_id)
    query = Q(is_specific=False)
    objects = DailyChores.objects.filter(query)
    for obj in objects:
        if is_current_week_in_range(obj.start_week, obj.end_week):
            TodoDailyChores.objects.create(
                market_garden=instance,
                daily_chores=obj,
            )

    specific_query = Q(is_specific=True, market_garden=instance)
    specific_objects = DailyChores.objects.filter(specific_query)

    if specific_objects:
        for obj in specific_objects:
            if is_current_week_in_range(obj.start_week, obj.end_week):
                TodoDailyChores.objects.create(
                    market_garden=instance,
                    daily_chores=obj,
                )


@shared_task
def create_todo_mulching(*args, **kwargs):
    instance_id = args[0]
    instance = get_object_or_404(MarketGarden, id=instance_id)
    TodoMulching.objects.create(
        market_garden=instance,
        mulching_rule=get_object_or_404(MulchingRule, name="Basic Rule"),
    )


@shared_task
def create_todo_watering(*args, **kwargs):
    instance_id = args[0]
    instance = get_object_or_404(WateringRule, id=instance_id)
    if is_current_week_in_range(instance.start_week, instance.end_week):
        TodoWatering.objects.create(
            market_garden=instance.market_garden,
            watering_rule=instance,
        )
