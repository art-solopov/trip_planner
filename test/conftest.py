import os
from collections import defaultdict
from tempfile import mkdtemp

import pytest
import pytest_mock

from passlib.hash import bcrypt

from trip_planner import db as _db, create_app
from trip_planner.models import User
from test import TestConfig, test_instance_dir
from . import factories as fc


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
    connection = db.engine.connect()
    transaction = connection.begin()

    session = db.create_scoped_session()
    db.session = session

    # Honestly I'm not sure how to make it more DRY
    # Maybe when I remove Flask-SQLAlchemy
    for factory in [fc.TripFactory, fc.UserFactory, fc.PointFactory]:
        factory._meta.sqlalchemy_session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope='session')
def app_client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def session_user(db_session):
    user = User(username='username',
                password_digest=bcrypt.hash('password'))
    with db_session.begin_nested() as trx:
        db_session.add(user)
        trx.commit()
    return user
