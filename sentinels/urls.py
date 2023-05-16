from django.urls import path
from django.views.generic import DetailView, ListView

from .apps import SentinelsConfig
from .models import Sentinel

app_name = SentinelsConfig.name
urlpatterns = [
    Sentinel.highlight_path,
    path(
        "detail/<slug:slug>",
        DetailView.as_view(model=Sentinel, template_name="sentinels/detail.html"),
        name="detail",
    ),
    path(
        "",
        ListView.as_view(model=Sentinel, template_name="sentinels/list.html"),
        name="list",
    ),
]
