from django.db import models
from django.conf import settings
from commons.models.base import BaseModel
from autoslug import AutoSlugField


class Section(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="Section Name",
        max_length=50,
        editable=True,
    )
    slug = AutoSlugField(
        verbose_name="Slug",
        populate_from="name",
        max_length=50,
        editable=True,
    )

    def __str__(self):
        return f"{self.user} - {self.name}"


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
        self.name = f"{self.section.name}{Bed.objects.count()+1}"
        super(Bed, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
