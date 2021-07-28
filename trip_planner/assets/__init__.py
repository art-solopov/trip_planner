import os.path as opa

from flask import Flask, Blueprint, current_app

assets = Blueprint('assets', __name__)

CHUNKS = ['commons', 'vendor',
          'shared_app']
# shared_app is not really a chunk, it's an app that controls flashes etc.
# It should be included in every page.


def chunks(app: Flask):
    return [chunk for chunk in CHUNKS
            if opa.exists(opa.join(
                    app.static_folder,
                    'js',
                    f'{chunk}.js'
            ))]


@assets.app_template_global('script_tag')
def script_tag(chunk: str) -> str:
    return f"<script src=\"/static/js/{chunk}.js\"></script>"


@assets.app_context_processor
def inject_js_chunks():
    return {
        'chunks': chunks(current_app)
    }
