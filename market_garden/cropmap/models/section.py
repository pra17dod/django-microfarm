from django.db import models
from commons.models.base import BaseModel
from autoslug import AutoSlugField
from market_garden.cropmap.models.cropmap import MarketGarden


class Section(BaseModel):
    market_garden = models.ForeignKey(
        MarketGarden,
        on_delete=models.CASCADE,
        verbose_name="Market Garden",
    )
    name = models.CharField(
        verbose_name="Section Name",
        max_length=50,
        editable=True,
        blank=True,
    )
    slug = AutoSlugField(
        verbose_name="Slug",
        populate_from="name",
        max_length=50,
        editable=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.name = f"Market Garden ID-{self.market_garden.id} Section{chr(ord('A') + Section.objects.filter(market_garden__id=self.market_garden.id).count())}"
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.market_garden.user} - {self.name}"


class Bed(BaseModel):
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="parent_section",
    )
    name = models.CharField(
        verbose_name="Bed Name",
        max_length=50,
        editable=True,
        blank=True,
    )
    status = models.IntegerField(
        verbose_name="Which season?",
        default=1,
        editable=True,
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.name = f"{self.section.name} Bed{Bed.objects.filter(section__id=self.section.id).count()+1}"
        super(Bed, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
