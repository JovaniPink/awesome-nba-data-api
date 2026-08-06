# Jinja templates

Templates in this directory are rendered by the Flask blueprints in
`app/views/`.

- `layout.html` provides shared page structure.
- `global.html` is the unauthenticated landing-page template.
- `pages/` contains route-specific templates, including the authenticated home
  page.

Keep static asset references compatible with Flask's `url_for('static', ...)`
behavior. When changing visible landing-page content, update the matching smoke
assertion in `test/test_app.py`.
