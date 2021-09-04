from pytest import fixture
from passlib.hash import bcrypt

from trip_planner import db
from trip_planner.models import User


@fixture(scope='function')
def session_user(app_client):
    user = User(username='username',
                password_digest=bcrypt.hash('password'))
    db.session.add(user)
    return user


def test_form_display(app_client):
    res = app_client.get('/login')
    assert res.status_code == 200
    assert b'<form' in res.data


def test_success_redirect(app_client, session_user):
    res = app_client.post('/login',
                          data=dict(username=session_user.username,
                                    password='password',
                                    redirect='/trips/'))
    assert res.status_code in range(300, 400)
    assert res.headers['Location'].endswith('/trips/')


def test_success_no_redirect(app_client, session_user):
    res = app_client.post('/login',
                          data=dict(username=session_user.username,
                                    password='password'))
    assert res.status_code in range(300, 400)
