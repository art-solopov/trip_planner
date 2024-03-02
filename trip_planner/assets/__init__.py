import os.path as opa
import json

from werkzeug.local import LocalProxy
from flask import Blueprint, current_app, url_for
from jinja2.ext import Markup

import assets.scripts.build as ab

assets = Blueprint('assets', __name__)


def load_manifest():
    manifest_path = opa.join(current_app.static_folder,
                             'assets', 'manifest.json')

    with open(manifest_path) as mff:
        return json.load(mff)


manifest = LocalProxy(load_manifest)


@assets.app_template_global('script_tag')
def script_tag(chunk_id: str) -> str:
    url = url_for('static', filename='assets/' + manifest[chunk_id + '.js'])
    return Markup(f'<script type="module" src="{url}"></script>')


@assets.app_template_global('style_tag')
def style_tag(style_name: str) -> str:
    url = url_for('static', filename='assets/' + manifest[style_name + '.css'])
    return Markup(f'<link rel="stylesheet" href="{url}" type="text/css">')


@assets.cli.command('build')
def assets_build():
    ab.main(current_app.static_folder)
