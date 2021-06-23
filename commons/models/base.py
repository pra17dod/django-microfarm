from django.db import models
from django.utils.timezone import now


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Created at",
        unique=False,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated at",
    )

    def save(self, *args, **kwargs):
        if not self.id or not self.created_at:
            self.created_at = now()
            self.updated_at = self.created_at
        else:
            self.updated_at = now()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
