from http import HTTPStatus

import pytest
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls.resolvers import URLPattern

from sentinels.models import Sentinel


def test_class_params():
    assert isinstance(Sentinel.highlight_path, URLPattern)
    assert (
        Sentinel.highlight_path.name
        == Sentinel._highlight_label
        == "highlight_sentinel"
    )


@pytest.mark.django_db
def test_highlightable_sentinel_attributes(client, a_sentinel):
    slug = "a-sample-title"
    url = a_sentinel.get_absolute_url()
    article = '<article id="highlightable">'
    response = client.get(url)

    assert a_sentinel.slug == slug
    assert a_sentinel.highlight_url == f"/highlight_sentinel/{slug}"
    assert url == f"/detail/{slug}"
    assert response.template_name == ["sentinels/detail.html"]
    assert isinstance(response, TemplateResponse)
    assert article in response.rendered_content


@pytest.mark.django_db
def test_add_highlight_post_anonymous(rf, a_sentinel):
    data = {"highlight": "Sample highlighted"}
    url = a_sentinel.highlight_url
    request = rf.post(url, data=data)
    request.user = AnonymousUser()
    response = Sentinel._save_highlight(request, a_sentinel.slug)
    assert isinstance(response, HttpResponseRedirect)
    assert response.status_code == HTTPStatus.FOUND


def test_add_highlight_post_authenticated(rf, a_highlighter, a_sentinel):
    # before
    data = {"highlight": "Sample highlighted"}
    url = a_sentinel.highlight_url
    counts = Count("highlights")
    pre = Sentinel.objects.aggregate(counts)
    assert pre["highlights__count"] == 0

    # during
    request = rf.post(url, data=data)
    request.user = a_highlighter
    response = Sentinel._save_highlight(request, a_sentinel.slug)

    # after
    post = Sentinel.objects.aggregate(counts)
    assert isinstance(response, HttpResponse)
    assert response.status_code == HTTPStatus.OK
    assert response.headers["HX-Trigger"] == "highlightSaved"
    assert post["highlights__count"] == 1
