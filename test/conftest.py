from collections import defaultdict
import logging

import pytest
import pytest_mock
from passlib.hash import bcrypt

from trip_planner import create_app, db
from trip_planner.models import User
from test import TestConfig, test_instance_dir, Session, db_session


@pytest.fixture(scope='session')
def app(session_mocker: pytest_mock.MockerFixture):
    _app = create_app(TestConfig(), instance_path=test_instance_dir)
    session_mocker.patch('trip_planner.assets.manifest',
                         new=defaultdict(str))

    return _app


@pytest.fixture(scope='session', autouse=True)
def bootstrap_db(app):
    sql_logger = logging.getLogger("sqlalchemy.engine")
    sql_logger.setLevel(logging.INFO)

    with app.app_context():
        db.create_all()

        yield

        db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def db_trx_session(app, caplog):
    caplog.set_level(logging.INFO)

    connection = db.engine.connect()
    transaction = connection.begin()
    Session.configure(bind=connection, join_transaction_mode='create_savepoint')

    with app.app_context():
        db.close_all_sessions()
        db.session = db_session
        yield db.session

        db.session.close()

    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def app_client(app):
    yield app.test_client()


@pytest.fixture(scope='function')
def session_user():
    print("Creating user")
    user = User(username='username',
                password_digest=bcrypt.hash('password'))
    db.session.add(user)
    db.session.commit()

    return user
