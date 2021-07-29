from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from market_garden.cropmap.models.cropmap import MarketGarden
from market_garden.cropmap.models.section import Section, Bed
from commons.scripts.location import get_timezone
from market_garden.cropmap.scripts.cropmap import Cropmap


@receiver(pre_save, sender=MarketGarden)
def calculate_cropmap(sender, instance, **kwargs):
    if not instance.timezone:
        instance.timezone = get_timezone(instance.latitude, instance.longitude)

    market_garden = Cropmap(
        instance.length,
        instance.width,
        instance.path_width,
        instance.path_width_btw_sections,
        instance.min_bed_length,
        instance.max_bed_length,
        instance.min_bed_per_section,
        instance.max_bed_per_section,
        instance.bed_width,
        instance.compost_height_of_bed,
        instance.compost_height_of_path,
    )
    (
        instance.bed_length,
        instance.bed_along_side_name,
        instance.num_of_bed_along_side,
        instance.num_of_bed_along_otherside,
        instance.bed_per_section,
        instance.total_sections,
        instance.area_used,
        instance.compost_required_per_bed,
        instance.total_compost_required,
    ) = market_garden.get_cropmap()


def create_bed(instance, num_of_bed_per_section=None):
    for _ in range(num_of_bed_per_section):
        Bed.objects.create(section=instance)


@receiver(post_save, sender=MarketGarden)
def create_section(sender, instance, created, **kwargs):
    if created:
        for _ in range(instance.total_sections):
            section = Section.objects.create(market_garden=instance)
            create_bed(section, instance.bed_per_section)
