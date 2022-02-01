# django-highlights

Add a generic relation `Highlight` to arbitrary models.

1. Selecting the highlight is done with custom javascript.
2. Saving the highlightted snippet (without page refresh) is done with `htmx` with a dash of `hyperscript` for dealing with the return trigger.

## Setup

### Install

```zsh
.venv> poetry add django-highlights # pip3 install django-highlights
```

### Add app to project settings

```python
# in project_folder/settings.py
INSTALLED_APPS = [
    ...,
    'highlights'
]
```

### Add highlight model to database

```zsh
.venv> python manage.py migrate
```

## Configuration

### Initialize model

Ensure model, e.g. `Sentinel`, with:

1. a _unique_ SlugField named `slug` - this will be used for creating the `highlight url`
2. a TextField, e.g. `content`/`description` - this is the field that will be _highlightable_

### Add mixin

Make the initialized model inherit from the `AbstractHighlightable` abstract base model :

```python
from django_extensions.db.models import TitleSlugDescriptionModel
from highlights.models import AbstractHighlightable # import
class Sentinel(TitleSlugDescriptionModel, AbstractHighlightable): # add
      pass
```

Each `Sentinel` instance, i.e. pk=1, pk=2, etc., will now have generic relations to a `Highlight` model and have access to a pre-named, `slug`-based `highlight_url`. The `Sentinel` class will now have a `@highlight_path` property to be used in `urlpatterns` so that each instances `highlight_url` is recognized by the project.

### Setup url

```python
# sentinels/urls.py
from .apps import SentinelsConfig # already built when you previously created `sentinels` via python manage.py startapp sentinels
from .models import Sentinel

app_name = SentinelsConfig.name # new
urlpatterns = [
    Sentinel.highlight_path, # new
    ...
]
```

### Use specific tag / ids

```jinja
<!-- sentinels/templates/sentinel_detail.html -->
<main class="container">
    <h1>Title: {{ object.title }}</h1>
    <article id="highlightable"> <!-- article id -->
        {{object.description}}
    </article>
</main>
{% if user.is_authenticated %}
    {% include 'highlights/footer.html' with save_highlight_url=object.highlight_url %} <!-- url -->
{% endif %}
```

## Flow

1. The `make_highlightable` templatetag produces an overridable template.
2. The template contains pre-id'ed html tags: `<article id='x'>` and `<footer id='y'>`
3. The `<article>` tag will contain the `scope` or the highlightable text field.
4. The `<footer>` will contain the `url` or the submission of highlights to the server.
5. The tags have event listeners sourced from `textSelector.js`.
6. Any text selection inside the `<article>` will reflect in the `<footer>`'s hidden `<input>`.
7. When highlight `maker` is ready with text selection, click on footer `<button>` submits highlight stored in `<input>`.
8. The submission is done through `htmx`'s `hx-post` without refreshing or swapping content, i.e. a POST request is sent to the `save_highlight` view c/o the passed `highlight_url`.
9. The request adds a new `Highlight` (from an authenticated highlight `maker`) to the highlightable model instance, e.g. Sentinel pk=2.
10. The addition sends a header trigger to the client to alert the `maker` (via `notyf.js` in tandem with `hyperscript`) that the highlight was successful.
