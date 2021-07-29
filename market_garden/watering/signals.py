from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from market_garden.watering.models.watering import WateringRule
import json
import pytz


@receiver(post_save, sender=WateringRule)
def create_watering_task(sender, instance, created, **kwargs):
    if created:
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute="00",
            hour="18",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone=pytz.timezone(instance.market_garden.timezone),
        )
        PeriodicTask.objects.create(
            crontab=schedule,
            name=f"{instance.market_garden.user}'s Watering Task ID-{instance.id}",
            task="market_garden.watering.tasks.check_watering_required",
            args=json.dumps([instance.id]),
            kwargs=json.dumps(
                {
                    "be_careful": True,
                }
            ),
        )
