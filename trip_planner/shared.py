from functools import wraps
from flask import g, redirect


def user_required(handler):
    @wraps(handler)
    def fn(*args, **kwargs):
        if g.user is None:
            return redirect("/login", 303)
        else:
            return handler(*args, **kwargs)
    return fn
