from flask import Blueprint, render_template, redirect, session, request, flash
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


def _render_login_form(form):
    return render_template('form.html', form=form,
                           title='Sign in',
                           submit_text='Login',
                           form_class='mx-auto w-64')


@auth.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate(form.username.data, form.password.data)
        if user is not None:
            session['user_id'] = user.id
            return redirect('/')
        else:
            flash('Incorrect login/password', 'error')
            return _render_login_form(form)
    return _render_login_form(form)


@auth.route('/logout', methods=('GET', 'POST'))
def logout():
    if request.method == 'POST':
        del session['user_id']
        return redirect('/')
    return render_template('confirm_form.html', submit_label='Log out')
