# django-highlights

Text selection and saving as generic relation Highlight on arbitrary models.

## Configuration

### Setup target

With an arbirary model, e.g. `Sentinel`, with a _unique_ `slug` and a target TextField, e.g. `content`, `description` that is desired to be _highlightable_, drop in `AbstractHighlightable` mixin:

```python
from django_extensions.db.models import TitleSlugDescriptionModel
class Sentinel(TitleSlugDescriptionModel, AbstractHighlightable):
      pass
```

Each `Sentinel` instance, i.e. pk=1, pk=2, etc., will now have generic relations to a `Highlight` model and have access to a pre-named, `slug`-based `highlight_url`.

### Use templatetag

The `highlight_url` and appropriate textfield of the highlightable model instance need to be passed to a `make_highlightable` templatetag in the highlightable model's "DetailView" template.

```jinja
<!-- sentinels/templates/sentinel_detail.html -->
{% load highlightable %} <!-- e.g. obj refers to the target model -->
{% make_highlightable scope=obj.description url=obj.highlight_url %}
```

A POST request sent to this url leads to the `save_highlight` view, adding a new `Highlight` from an authenticated highlight`maker` to the target highlightable, e.g. Sentinel pk=2.

## Flow

1. The `make_highlightable` templatetag produces an overridable template.
2. The template contains pre-id'ed `<article id='x'>` and `<footer id='y'>` html tags.
3. The html tags are associated event listeners preconfigured by a loaded custom `highlighter.js`.
4. The `<article>` tag will contain the `scope` or the highlightable text field.
5. The `<footer>` will contain the `url` or the submission of highlights to the server.
6. With this setup, any text selection made inside the `<article>` will reflect in the `<footer>`.
7. When the highlight `maker` is ready with a proper text selection, can click on the button in the footer to submit the highlight.
8. The submission is done through `htmx`'s `hx-post` without refreshing or swapping content.
9. A successful submission results in the creation of a new `Highlight` made by an authenticated `maker` and a trigger to the client to alert the `maker` (via `notyf.js` in tandem with `hyperscript`)
