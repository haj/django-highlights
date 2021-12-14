import uuid

from django.db import models
from django.urls import reverse
from django_extensions.db.models import TitleSlugDescriptionModel

from highlights.models import AbstractHighlightable


class Sentinel(TitleSlugDescriptionModel, AbstractHighlightable):
    """Presumption: Concrete model will make use of `title`, `slug` and a content-based TextField. The `slug` must be unique. Each sentinel instance will now have a generic relations to a `Highlight` model and a pre-named `highlight_url`."""

    ...

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(f"{self._meta.app_label}:detail", args=[self.slug])
