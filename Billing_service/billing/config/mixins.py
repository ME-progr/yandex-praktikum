import uuid

from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    class Meta:
        abstract = True


class TimeStampedModelMixin:
    created_at = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Абстрактная модель для добавления полей в другие модели."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        null=False,
        blank=True,
        unique=True
    )

    class Meta:
        abstract = True
