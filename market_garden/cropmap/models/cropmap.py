from django.db import models
from django.conf import settings
from commons.models.farm import FarmModel


class MarketGarden(FarmModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    path_width = models.DecimalField(
        verbose_name="Path Width (in m)",
        max_digits=3,
        decimal_places=2,
        default=0.4,
        blank=True,
    )
    path_width_btw_sections = models.DecimalField(
        verbose_name="Path Width between Sections (in m)",
        max_digits=3,
        decimal_places=2,
        default=0.7,
        blank=True,
    )
    min_bed_length = models.DecimalField(
        verbose_name="Minimum Bed Length (in m)",
        max_digits=3,
        decimal_places=1,
        default=5.0,
        blank=True,
    )
    max_bed_length = models.DecimalField(
        verbose_name="Maximum Bed Length (in m)",
        max_digits=3,
        decimal_places=1,
        default=25.0,
        blank=True,
    )
    min_bed_per_section = models.IntegerField(
        verbose_name="Minimum Bed per Section",
        default=1,
        blank=True,
    )
    max_bed_per_section = models.IntegerField(
        verbose_name="Maximum Bed per Section",
        default=10,
        blank=True,
    )
    bed_length = models.DecimalField(
        verbose_name="Bed Length (in m)",
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
    )
    bed_width = models.DecimalField(
        verbose_name="Bed Width (in m)",
        max_digits=3,
        decimal_places=2,
        default=0.75,
        blank=True,
        null=True,
    )
    bed_along_side_name = models.CharField(
        verbose_name="Side Along which Bed are made",
        max_length=50,
        blank=True,
        null=True,
    )
    num_of_bed_along_side = models.IntegerField(
        verbose_name="No. of Bed Along Side",
        blank=True,
        null=True,
    )
    num_of_bed_along_otherside = models.IntegerField(
        verbose_name="No. of Bed Along Otherside",
        blank=True,
        null=True,
    )
    bed_per_section = models.IntegerField(
        verbose_name="Bed per Section",
        blank=True,
        null=True,
    )
    total_sections = models.IntegerField(
        verbose_name="Total Sections",
        blank=True,
        null=True,
    )
    area_used = models.DecimalField(
        verbose_name="Area Used(in %)",
        max_digits=4,
        decimal_places=2,
        blank=True,
        null=True,
    )
    compost_height_of_bed = models.DecimalField(
        verbose_name="Compost Height of Bed (in m)",
        max_digits=3,
        decimal_places=2,
        default=0.3,
        blank=True,
        null=True,
    )
    compost_height_of_path = models.DecimalField(
        verbose_name="Compost Height of Path (in m)",
        max_digits=3,
        decimal_places=2,
        default=0.1,
        blank=True,
        null=True,
    )
    compost_required_per_bed = models.DecimalField(
        verbose_name="Compost Required per Bed (in cu.m)",
        max_digits=9,
        decimal_places=1,
        blank=True,
        null=True,
    )
    total_compost_required = models.DecimalField(
        verbose_name="Total Compost Required (in cu.m)",
        max_digits=9,
        decimal_places=1,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Market Garden"

    def __str__(self):
        return f"{self.user}'s Market Garden"
