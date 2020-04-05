from functools import wraps
from collections import namedtuple

from flask import g, redirect


def user_required(handler):
    @wraps(handler)
    def fn(*args, **kwargs):
        if g.user is None:
            return redirect("/login", 303)
        else:
            return handler(*args, **kwargs)
    return fn


Breadcrumb = namedtuple('Breadcrumb', ['text', 'link'])


def add_breadcrumb(text, link=None):
    g.breadcrumbs.append(Breadcrumb(text, link))
