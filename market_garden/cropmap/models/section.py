from django.db import models
from rest_framework import serializers
from commons.models.base import BaseModel
from autoslug import AutoSlugField
from market_garden.cropmap.models.cropmap import MarketGarden
from commons.scripts.get_user_id import get_user_id
from django.shortcuts import get_object_or_404


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

    class Meta:
        verbose_name_plural = "02 Sections"

    def __str__(self):
        return f"{self.market_garden.user} - {self.name}"


class SectionSerializer(serializers.ModelSerializer):
    def validate_market_garden_owner(self, data):
        market_garden = get_object_or_404(MarketGarden, pk=data["market_garden"])
        if get_user_id(self.request)["user_id"] != market_garden.user:
            raise serializers.ValidationError(
                "You are not the owner of this market-garden"
            )
        return data

    class Meta:
        model = Section
        fields = "__all__"


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

    class Meta:
        verbose_name_plural = "03 Beds"

    def __str__(self):
        return self.name


class BedSerializer(serializers.ModelSerializer):
    def validate_section_owner(self, data):
        section = get_object_or_404(Section, pk=data["section"])
        if get_user_id(self.request)["user_id"] != section.market_garden.user:
            raise serializers.ValidationError(
                "You are not the owner of this market-garden"
            )
        return data

    class Meta:
        model = Bed
        fields = "__all__"
