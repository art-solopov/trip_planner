import os.path as opa
import json

from flask import Blueprint, current_app, url_for, g
from jinja2.ext import Markup

assets = Blueprint('assets', __name__)


@assets.before_app_request
def load_manifest():
    manifest_path = opa.join(current_app.static_folder,
                             'assets', 'manifest.json')

    with open(manifest_path) as mff:
        g.assets_manifest = json.load(mff)


@assets.app_template_global('script_tag')
def script_tag(chunk_id: str) -> str:
    url = url_for('static', filename=g.assets_manifest[chunk_id])
    return Markup(f'<script type="module" src="{url}"></script>')


@assets.app_template_global('style_tag')
def style_tag(style_name: str) -> str:
    url = url_for('static', filename=g.assets_manifest[style_name + '.css'])
    return Markup(f'<link rel="stylesheet" href="{url}" type="text/css">')
