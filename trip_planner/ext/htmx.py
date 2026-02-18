from flask import Flask, request


class HTMX:
    def __init__(self, app: Flask | None = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        app.context_processor(lambda: {'htmx': self})

    @property
    def is_htmx(self) -> bool:
        """Returns true if the request was sent with HTMX"""
        return request.headers.get('HX-Request') is not None

    @property
    def is_boosted(self) -> bool:
        return request.headers.get('HX-Boosted') is not None

    @property
    def target(self) -> str | None:
        return request.headers.get('HX-Target')
