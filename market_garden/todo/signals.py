from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from market_garden.watering.models.watering_rule import WateringRule
from market_garden.cropmap.models.cropmap import MarketGarden
from market_garden.todo.tasks import create_todo_mulching
import json
import pytz


@receiver(post_save, sender=MarketGarden)
def create_todo_daily_chores_task(sender, instance, created, **kwargs):
    if created:
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute="*",
            hour="6",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone=pytz.timezone(instance.timezone),
        )
        PeriodicTask.objects.create(
            crontab=schedule,
            name=f"{instance.user}'s MarketGarden ID-{instance.id} Todo DailyChores",
            task="market_garden.todo.tasks.create_todo_daily_chores",
            args=json.dumps([instance.id]),
            kwargs=json.dumps(
                {
                    "be_careful": True,
                }
            ),
        )


@receiver(post_save, sender=MarketGarden)
def create_todo_mulching_task(sender, instance, created, **kwargs):
    if created:
        create_todo_mulching.apply_async(args=[instance.id], kwargs={}, countdown=5)


@receiver(post_save, sender=WateringRule)
def create_todo_watering_task(sender, instance, created, **kwargs):
    if created:
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute="*",
            hour="6",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone=pytz.timezone(instance.market_garden.timezone),
        )
        PeriodicTask.objects.create(
            crontab=schedule,
            name=f"{instance.market_garden.user}'s MarketGarden ID-{instance.id} Todo Watering",
            task="market_garden.todo.tasks.create_todo_watering",
            args=json.dumps([instance.id]),
            kwargs=json.dumps(
                {
                    "be_careful": True,
                }
            ),
        )
