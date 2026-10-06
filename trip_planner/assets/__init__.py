import os.path as opa
import json
import subprocess as sp

from werkzeug.local import LocalProxy
from flask import Blueprint, current_app, url_for
from jinja2.ext import Markup

assets = Blueprint('assets', __name__)


def _load_manifest():
    manifest_path = opa.join(current_app.static_folder,
                             '.vite', 'manifest.json')

    with open(manifest_path) as mff:
        return json.load(mff)


_use_manifest = LocalProxy(lambda: 'VITE_SERVER' not in current_app.config)
manifest = LocalProxy(_load_manifest)


@assets.app_template_global('vite_script')
def vite_script(script_name: str) -> str:
    entry = f'js/{script_name}.js'
    if _use_manifest:
        tags = [style_tag(url_for('static', filename=h)) for h in _script_style_deps(entry)]

        url = url_for('static', filename=manifest[entry]['file'])
        tags.append(script_tag(url))
        return Markup("\n".join(tags))
    else:
        return script_tag(current_app.config['VITE_SERVER'] + '/' + entry)


@assets.app_template_global('vite_style')
def vite_style(style_name: str) -> str:
    entry = f'css/{style_name}'  # Don't add extension because some of it is scss
    if _use_manifest:
        filename = manifest[entry]['file']
        url = url_for('static', filename=filename)
        return style_tag(url)
    else:
        return style_tag(current_app.config['VITE_SERVER'] + '/' + entry)


def _script_style_deps(script_name: str):
    manifest_data = manifest[script_name]
    if (css_data := manifest_data.get('css', None)):
        yield from css_data
    if (imports := manifest_data.get('imports', None)):
        for ipt in imports:
            yield from _script_style_deps(ipt)


def script_tag(src):
    return Markup(f'<script type="module" src="{src}"></script>')


def style_tag(href):
    return Markup(f'<link rel="stylesheet" href="{href}" type="text/css">')


@assets.cli.command(('build'))
def assets_build():
    sp.run(['pnpm', 'vite', 'build'])
