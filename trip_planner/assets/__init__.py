import os.path as opa
import json
import logging

from werkzeug.local import LocalProxy
from flask import Blueprint, current_app, url_for
from jinja2.ext import Markup

assets = Blueprint('assets', __name__)
logger = logging.getLogger(__name__)


def _compute_vite_manifest_path():
    return opa.join(current_app.static_folder, '.vite', 'manifest.json')


_vite_manifest_path = LocalProxy(_compute_vite_manifest_path)


def _load_manifest():
    logger.info("Loading manifest")
    with open(_vite_manifest_path) as mff:
        return json.load(mff)


manifest = LocalProxy(_load_manifest)


@assets.app_template_global('script_tag')
def script_tag(chunk_id: str) -> str:
    url = url_for('static', filename=manifest[chunk_id + '.js'])
    return Markup(f'<script type="module" src="{url}"></script>')


@assets.app_template_global('style_tag')
def style_tag(style_name: str) -> str:
    url = url_for('static', filename=manifest[style_name + '.css'])
    return Markup(f'<link rel="stylesheet" href="{url}" type="text/css">')
