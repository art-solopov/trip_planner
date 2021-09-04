from functools import wraps
from collections import namedtuple

from flask import g, redirect, url_for, request


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
