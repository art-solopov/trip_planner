from os import getenv
from os import path as path

from sqlalchemy.orm import sessionmaker, scoped_session

from trip_planner.config import Config


Session = sessionmaker()
db_session = scoped_session(Session)


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'testsecret'
    SERVER_NAME = 'test.test'  # For url_for generation

    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = getenv(
            'TESTDB', 'postgresql:///trip_planner_test'
        )


test_instance_dir = path.join(
    path.dirname(path.abspath(__file__)),
    'instance'
)
