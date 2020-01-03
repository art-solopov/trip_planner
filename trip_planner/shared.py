from functools import wraps
from flask import g, redirect


def user_requred(handler):
    @wraps(handler)
    def fn(*args, **kwargs):
        if g.user is None:
            redirect("/login", 303)
        else:
            return handler(*args, **kwargs)
    return fn
