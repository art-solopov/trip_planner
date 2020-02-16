from flask.ctx import AppContext
from flask.wrappers import Response
from flask.testing import FlaskClient
from passlib.hash import bcrypt

from trip_planner import create_app, db
from trip_planner.models import User

test_config = {
    'SQLALCHEMY_DATABASE_URI': 'postgresql:///trip_planner_test',
    'TESTING': True,
    'WTF_CSRF_ENABLED': False,
}

app = create_app(test_config)


def setup_module():
    with app.test_client():
        with app.app_context():
            db.create_all()


def teardown_module():
    with app.test_client():
        with app.app_context():
            db.drop_all()


def login(client: FlaskClient, username: str, password: str):
    return client.post('/login', data=dict(username=username,
                                           password=password))


class WithTestClient:
    @classmethod
    def setup_class(cls):
        cls.client = app.test_client()

    def login(self, username: str, password: str) -> Response:
        return login(self.client, username, password)

    def logout(self):
        return self.client.post('/logout')


class WithAppContext:
    _app_context: AppContext = None

    def setUp(self):
        self._app_context = app.app_context()
        self._app_context.push()
        super().setUp()

    def tearDown(self):
        self._app_context.pop()


class WithDB(WithAppContext):
    def setUp(self):
        super().setUp()
        self._transaction = db.session.begin_nested()

    def tearDown(self):
        db.session.rollback()
        super().tearDown()


class WithUser(WithDB):
    username = 'user'
    password = 'password'
    user = User(username=username, password_digest=bcrypt.hash(password))

    def setUp(self):
        super().setUp()
        db.session.add(self.user)
        db.session.flush()


class WithLogin(WithUser, WithTestClient):
    def setUp(self):
        super().setUp()
        self.login(self.username, self.password)
