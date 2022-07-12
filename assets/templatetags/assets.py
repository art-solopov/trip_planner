import json
from functools import cache

from django import template
from django.conf import settings
from django.utils.html import format_html

register = template.Library()


def _read_manifest():
    # TODO: extract into settings
    path = 'assets/static/manifest.json'
    with open(path) as f:
        return json.load(f)


if not settings.DEBUG:
    _read_manifest = cache(_read_manifest)


@register.simple_tag
def asset_script_tag(name: str, is_module: bool = True):
    script_path = _read_manifest()[name]
    script_type = 'module' if is_module else 'text/javascript'
    return format_html('<script type="{}" src="{}"></script>',
                       script_type, script_path)


@register.simple_tag
def asset_style_tag(name: str):
    style_path = _read_manifest()[name + '.css']
    return format_html('<link rel="stylesheet" href="{}">', style_path)


@register.simple_tag
def htmx_tag():
    version = settings.HTMX_VERSION
    path = f"{settings.STATIC_URL}vendor/htmx-{version}.min.js"
    return format_html('<script src="{}"></script>', path)
