import uuid

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

    def __str__(self):
        return (
            f"{self.content[:15]}... by {self.maker}"
            or "No content in {self.id} by {self.maker}"
        )


class AbstractHighlightable(TitleSlugDescriptionModel, TimeStampedModel):
    content = models.TextField()
    highlights = GenericRelation(
        Highlight, related_query_name="%(app_label)s_%(class)ss"
    )

    class Meta:
        abstract = True

    @property
    def get_highlight_url(self) -> str:
        named_route = f"{self._meta.app_label}:{self._label}"
        return reverse(named_route, args=(self.slug,))

    @classproperty
    def _label(cls) -> str:
        return f"highlight_{cls._meta.model_name}"

    @classproperty
    def highlight_path(cls) -> URLPattern:
        return path(
            f"{cls._label}/<slug:slug>", cls._save_highlight, name=cls._label
        )

    @classmethod
    def _save_highlight(cls, request: HttpRequest, slug: str) -> HttpResponse:
        if not request.user.is_authenticated:  # required to highlight
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

        highlight = Highlight(
            content=request.POST.get("highlight"),
            maker=request.user,
            content_object=cls.objects.get(slug=slug),
        )
        highlight.save()

        return HttpResponse(request, headers={"HX-Trigger": "highlightSaved"})
