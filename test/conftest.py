import os
from collections import defaultdict
from tempfile import mkdtemp

import pytest
import pytest_mock
from passlib.hash import bcrypt

from trip_planner import db as _db
from trip_planner.models import User
from test import create_app, TestConfig, test_instance_dir


@pytest.fixture(scope='session')
def app(session_mocker: pytest_mock.MockerFixture):
    static_folder = mkdtemp(prefix='static')
    _app = create_app(TestConfig(), instance_path=test_instance_dir,
                      static_folder=static_folder)
    ctx = _app.app_context()
    ctx.push()
    session_mocker.patch('trip_planner.assets.manifest',
                         new=defaultdict(str))

    yield _app

    ctx.pop()
    os.rmdir(static_folder)


@pytest.fixture(scope='session')
def db(app):
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def db_session(db):
    yield db.session

    db.session.remove()


@pytest.fixture(scope='session')
def app_client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def session_user(db_session):
    user = User(username='username',
                password_digest=bcrypt.hash('password'))
    db_session.add(user)
    return user
