from flask import Blueprint, render_template, redirect, session
from passlib.hash import bcrypt
from .forms import LoginForm
from ..models import User

auth = Blueprint('auth', __name__)


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    if bcrypt.verify(password, user.password_digest):
        return user
    else:
        return None


@auth.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate(form.username.data, form.password.data)
        if user is not None:
            session['user_id'] = user.id
            return redirect('/')
        else:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)
