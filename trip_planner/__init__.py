import os.path

from flask import Flask, render_template, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from wtforms import Field


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

from .auth import auth as auth_bp  # noqa: E402
from .trips import trips as trips_bp  # noqa: E402
from .api import api as api_bp  # noqa: E402
from .models import User  # noqa: E402


def create_app(test_config=None, **kwargs):
    app = Flask(__name__, **kwargs)

    app.config.from_mapping(
        SECRET_KEY='LC!4.0tmi06@0J~YXiqjHVkCU3x1vDhA',
        SQLALCHEMY_DATABASE_URI='postgresql:///trip_planner',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SQLALCHEMY_ECHO=True,
        SECRETS_PATH=os.path.join(app.instance_path, 'secrets.json'),
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    if app.config['SECRETS_PATH'] is not None:
        app.config.from_json(app.config['SECRETS_PATH'])

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    @app.before_request
    def init_breadcrumbs():
        g.breadcrumbs = []

    @app.before_request
    def get_user():
        try:
            user_id = session['user_id']
            if user_id is None:
                g.user = None
                return
            g.user = User.query.filter_by(id=user_id).first()
        except KeyError:
            g.user = None
            return

    @app.route("/")
    def root():
        return render_template('root.html')

    app.register_blueprint(auth_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(api_bp)

    @app.template_test('hidden_field')
    def is_hidden_field(field: Field) -> bool:
        return field.widget.input_type == 'hidden'

    if app.env == 'development':
        import IPython

        @app.cli.command('ishell')
        def ishell():
            IPython.start_ipython(argv=[])

    return app
