from __future__ import absolute_import, unicode_literals

from celery import shared_task
from market_garden.cropmap.models.cropmap import MarketGarden
from market_garden.cropmap.models.section import Section, Bed
from django.shortcuts import get_object_or_404
from django.utils import timezone


def create_bed(instance, num_of_bed_per_section=None):
    for _ in range(num_of_bed_per_section):
        Bed.objects.create(section=instance)


@shared_task
def create_section_bed(*args, **kwargs):
    instance_id = args[0]
    instance = get_object_or_404(MarketGarden, id=instance_id)

    for _ in range(instance.total_sections):
        section = Section.objects.create(market_garden=instance)
        create_bed(section, instance.bed_per_section)
