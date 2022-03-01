from functools import wraps
from collections import namedtuple
from decimal import Decimal

from flask import g, redirect, url_for, request
from werkzeug.routing import BaseConverter


def user_required(handler):
    @wraps(handler)
    def fn(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', r=request.path), 303)
        else:
            return handler(*args, **kwargs)
    return fn


Breadcrumb = namedtuple('Breadcrumb', ['text', 'link'])


def add_breadcrumb(text, link=None):
    g.breadcrumbs.append(Breadcrumb(text, link))


class DecimalPairConverter(BaseConverter):
    regex = r'\d+(\.\d+)?,\d+(\.\d+)?'

    def to_python(self, value: str):
        return tuple(Decimal(cmp) for cmp in value.split(','))

    def to_url(self, value):
        return f'{value[0]},{value[1]}'
