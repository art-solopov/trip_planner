import pytest

from trip_planner import db as _db
from test import create_app, TestConfig, test_instance_dir


@pytest.fixture(scope='session')
def app():
    _app = create_app(TestConfig(), instance_path=test_instance_dir)
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


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

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope='session')
def app_client(app):
    return app.test_client()
