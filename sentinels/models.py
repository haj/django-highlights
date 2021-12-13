import uuid

from django.db import models
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from django.urls import URLPattern, reverse
from django.utils.functional import classproperty

from highlights.models import AbstractHighlightable


class Sentinel(AbstractHighlightable):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(f"{self._meta.app_label}:detail", args=[self.slug])
