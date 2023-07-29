from urllib.parse import urlparse
import string
import random

from flask import Blueprint, render_template, redirect, session, request, flash, g
import click
from passlib.context import CryptContext
from .forms import LoginForm, PasswordChangeForm
from .. import db
from ..models import User
from ..bs_classes import ViewClasses

auth = Blueprint('auth', __name__)


_passlib_context = CryptContext(schemes=['bcrypt'])


def _authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return None
    if _passlib_context.verify(password, user.password_digest):
        return user
    else:
        return None


def _render_login_form(form):
    return render_template('form.html', form=form,
                           title='Sign in',
                           submit_text='Login',
                           form_class=ViewClasses.LOGIN_FORM)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = _authenticate(form.username.data, form.password.data)
        if user is not None:
            session['user_id'] = user.id
            session.permanent = True
            flash('Login successful', 'success')
            return redirect(form.redirect.data or '/')
        else:
            flash('Incorrect login/password', 'danger')
            return _render_login_form(form)
    try:
        form.redirect.data = urlparse(request.args['r']).path
    except KeyError:
        pass  # If r is not in request args, do nothing
    return _render_login_form(form)


@auth.route('/logout', methods=('GET', 'POST'))
def logout():
    if request.method == 'POST':
        del session['user_id']
        return redirect('/')
    return render_template('confirm_form.html', message='Are you sure you want to sign out?',
                           submit_label='Sign out')


def _update_password(user, password):
    user.password_digest = _passlib_context.hash(password)
    db.session.add(user)


def _render_password_change_form(form):
    return render_template('form.html', form=form, title='Change password',
                           submit_text='Change password')


@auth.route('/change_password', methods=('GET', 'POST'))
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if _passlib_context.verify(form.current_password.data, g.user.password_digest):
            _update_password(g.user, form.new_password.data)
            db.session.commit()
            flash('Password changed', 'success')
            return redirect('/')
        else:
            flash('Incorrect password', 'danger')
            return _render_password_change_form(form)
    else:
        return _render_password_change_form(form)


def _gen_password():
    yield random.choice(string.ascii_uppercase)
    yield from random.sample(string.digits, 2)
    yield from random.sample(string.ascii_lowercase, 3)
    yield from random.sample(string.ascii_letters, 4)


@auth.cli.command('makeuser')
@click.argument('username')
def makeuser(username):
    user = User(username=username)
    password = ''.join(_gen_password())
    _update_password(user, password)
    db.session.commit()
    print(f"Created user with username={username}; password={password}")
