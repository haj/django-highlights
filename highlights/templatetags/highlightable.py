from django import template

register = template.Library()


@register.inclusion_tag("highlights/skeletal_frame.html", takes_context=True)
def make_highlightable(
    context,
    scope: str,
    url: str,
):
    context["highlightable_content"] = scope
    context["save_highlight_url"] = url
    return context
