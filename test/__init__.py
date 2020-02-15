from flask.ctx import AppContext

from trip_planner import create_app, db

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


class WithTestClient:
    @classmethod
    def setup_class(cls):
        cls.client = app.test_client()


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
