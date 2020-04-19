from os import getenv
from os import path as path

from flask.ctx import AppContext
from flask.wrappers import Response
from flask.testing import FlaskClient
from passlib.hash import bcrypt

from trip_planner import create_app
from trip_planner.config import Config
from trip_planner.models import User


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'testsecret'

    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = getenv(
            'TESTDB', 'postgresql:///trip_planner_test'
        )


test_instance_dir = path.join(
    path.dirname(path.abspath(__file__)),
    'instance'
)
