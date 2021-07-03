import os.path as opa

from flask import Flask

# TODO: make it an app plugin?

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


def script_tag(chunk: str) -> str:
    return f"<script src=\"/static/js/{chunk}.js\"></script>"
