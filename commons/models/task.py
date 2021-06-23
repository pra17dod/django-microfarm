from django.db import models
from commons.models.base import BaseModel
from autoslug import AutoSlugField


class TaskModel(BaseModel):
    name = models.CharField(
        verbose_name="Name",
        max_length=50,
        editable=True,
    )
    slug = AutoSlugField(
        verbose_name="Slug",
        populate_from="name",
        max_length=50,
        editable=True,
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=500,
        editable=True,
        blank=True,
        null=True,
    )
    guide = models.TextField(
        verbose_name="How to Do?",
        max_length=1000,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        verbose_name="Image",
        blank=True,
        null=True,
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

    class Meta:
        abstract = True
