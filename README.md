# django-highlights

Text selection and saving as generic relation Highlight on arbitrary models.

## Configuration

### Setup target

Presumes a highlightable model, e.g. `Sentinel` with "highlightable" TextField, e.g. `content`, `description`, etc. characterized by a `AbstractHighlightable` abstract base model.

```python
from django_extensions.db.models import TitleSlugDescriptionModel
class Sentinel(TitleSlugDescriptionModel, AbstractHighlightable):
      """Presumption: Concrete model will make use of `title`, `slug` and a content-based TextField, e.g. `description`. The `slug` must be unique. Each sentinel instance will now have a generic relations to a `Highlight` model and a pre-named `highlight_url`."""
      ...# In this case, the `description` can be used as an example TextField
```

The mixin auto-generates a slug-based `highlight_url` connected to a POST-based `save_highlight` view function.

### Use templatetag

The `highlight_url` and appropriate textfield of the highlightable model instance need to be passed to a `make_highlightable` templatetag in the highlightable model's "DetailView" template.

```jinja
<!-- sentinels/templates/sentinel_detail.html -->
{% load highlightable %}
{% make_highlightable scope=object.description url=object.highlight_url %} <!-- Assume object refers to the target model -->
```

## How {% make_highlightable %} works

1. The `make_highlightable` templatetag produces an overridable template.
2. The template contains pre-id'ed `<article id='x'>` and `<footer id='y'>` html tags.
3. The html tags are associated event listeners preconfigured by a loaded custom `highlighter.js`.
4. The `<article>` tag will contain the `scope` or the highlightable text field.
5. The `<footer>` will contain the `url` or the submission of highlights to the server.
6. With this setup, any text selection made inside the `<article>` will reflect in the `<footer>`.
7. When the highlight `maker` is ready with a proper text selection, can click on the button in the footer to submit the highlight.
8. The submission is done through `htmx`'s `hx-post` without refreshing or swapping content.
9. A successful submission results in the creation of a new `Highlight` made by an authenticated `maker` and a trigger to the client to alert the `maker` (via `notyf.js` in tandem with `hyperscript`)
