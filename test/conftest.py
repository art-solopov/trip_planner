from collections import defaultdict
# import logging

import pytest
import pytest_mock
from passlib.hash import bcrypt

from trip_planner import create_app, db as _db
from trip_planner.models import User
from test import TestConfig, test_instance_dir


@pytest.fixture(scope='session')
def app(session_mocker: pytest_mock.MockerFixture):
    _app = create_app(TestConfig(), instance_path=test_instance_dir)
    session_mocker.patch('trip_planner.assets.manifest',
                         new=defaultdict(str))

    return _app


@pytest.fixture(scope='session')
def db(app):
    with app.app_context():
        _db.create_all()

        yield _db

        _db.drop_all()


# @pytest.fixture(scope='session', autouse=True)
# def _db_log():
#     logger = logging.getLogger('sqlalchemy.engine')
#     logger.setLevel('DEBUG')
#
#     handler = logging.FileHandler('log/sql-test.log')
#     handler.setFormatter(logging.Formatter())
#     logger.addHandler(handler)


@pytest.fixture(scope='function', autouse=True)
def _cleanup_db(app, db):
    yield

    with app.app_context():
        tables = list(db.Model.metadata.tables.keys())
        tables.reverse()
        tables = ', '.join(tables)
        db.session.execute(db.text(f'TRUNCATE {tables} CASCADE'))
        db.session.commit()


@pytest.fixture(scope='function')
def db_session(app, db):
    with app.app_context():
        yield db.session

        db.session.remove()


@pytest.fixture(scope='function')
def app_client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def session_user(db_session):
    user = User(username='username',
                password_digest=bcrypt.hash('password'))
    db_session.add(user)
    db_session.commit()
    return user
