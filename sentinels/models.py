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

    @classmethod
    def add_highlight_func(cls, request, slug: str) -> HttpResponse:
        target_obj = cls.objects.get(slug=slug)
        return cls.save_highlight(request, target_obj)

    @classproperty
    def add_highlight_path(cls) -> URLPattern:
        return cls.set_highlight_path("<slug:slug>", cls.add_highlight_func)
