from django.db import models
from commons.models.base import BaseModel
from autoslug import AutoSlugField


class RuleModel(BaseModel):
    name = models.CharField(
        verbose_name="Rule Name",
        max_length=50,
        editable=True,
    )
    slug = AutoSlugField(
        verbose_name="Slug",
        populate_from="name",
        max_length=50,
        editable=True,
        blank=True,
    )
    string = models.CharField(
        verbose_name="String value",
        max_length=50,
        editable=True,
        blank=True,
        null=True,
    )
    numerical = models.IntegerField(
        verbose_name="Numerical value",
        editable=True,
        blank=True,
        null=True,
    )
    boolean = models.BooleanField(
        verbose_name="Boolean value",
        editable=True,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
