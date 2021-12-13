import uuid
from typing import Callable

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import URLPattern, path, reverse
from django.utils.functional import classproperty
from django_extensions.db.models import (
    TimeStampedModel,
    TitleSlugDescriptionModel,
)


class Highlight(TimeStampedModel):
    """The `AbstractHighlightable` model has a highlights field which map to this model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # main fields
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    maker = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="highlights"
    )

    # generic fk base, uses CharField to accomodate sentinel models with UUID as primary key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey("content_type", "object_id")


class AbstractHighlightable(TitleSlugDescriptionModel, TimeStampedModel):
    content = models.TextField()
    highlights = GenericRelation(
        Highlight, related_query_name="%(app_label)s_%(class)ss"
    )

    class Meta:
        abstract = True

    @classproperty
    def _label(cls) -> str:
        return f"highlight_{cls._meta.model_name}"

    @property
    def get_highlight_url(self) -> str:
        return reverse(
            f"{self._meta.app_label}:{self._label}", args=(self.slug,)
        )

    @classmethod
    def set_highlight_path(
        cls, endpoint_token: str, func_comment: Callable
    ) -> URLPattern:
        return path(
            f"{cls._label}/{endpoint_token}", func_comment, name=cls._label
        )

    @classmethod
    def save_highlight(cls, request: HttpRequest, target_obj):

        if not request.user.is_authenticated:  # required to highlight
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

        highlight = Highlight(
            content=request.POST.get("highlight"),
            maker=request.user,
            content_object=target_obj,
        )
        highlight.save()

        return HttpResponse(request, headers={"HX-Trigger": "highlightSaved"})
