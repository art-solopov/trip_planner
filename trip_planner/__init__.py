import os
import os.path
import json
import logging

from flask import Flask, render_template, request, session, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from wtforms import Field
from markupsafe import Markup

from .shared import DecimalPairConverter


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

DATA_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'data'
    )
)


from .auth import auth as auth_bp  # noqa: E402
from .trips import trips as trips_bp  # noqa: E402
from .pjax import pjax as pjax_bp  # noqa: E402
from .scripts import scripts as scripts_bp  # noqa: E402
from .assets import assets as assets_bp  # noqa: E402
from .models import User  # noqa: E402


def create_app(test_config=None, instance_path=None, static_folder='static'):
    if instance_path is None:
        env_instance_path = os.getenv('INSTANCE_PATH')
        if env_instance_path:
            instance_path = env_instance_path

    app = Flask(__name__,
                instance_path=instance_path,
                instance_relative_config=True,
                static_folder=static_folder)
    if test_config is not None:
        app.config.from_object(test_config)
    else:
        # TODO: probably replace with something better?
        app_env = os.getenv('FLASK_ENV') or 'production'
        app.config.from_object(f'trip_planner.config.{app_env.capitalize()}')

    secrets_path = app.config['SECRETS_PATH']
    if secrets_path:
        app.config.from_file(secrets_path, load=json.load) #  TODO: replace with TOML?

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    app.url_map.converters['decimal_pair'] = DecimalPairConverter

    # TODO configure logging properly
    if app.debug:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

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
    app.register_blueprint(pjax_bp)
    app.register_blueprint(scripts_bp)
    app.register_blueprint(assets_bp)

    @app.template_test('hidden_field')
    def is_hidden_field(field: Field) -> bool:
        return getattr(field.widget, 'input_type', '') == 'hidden'

    @app.context_processor
    def inject_form_base_template():
        flag = ('true' in request.args.getlist('for_dialog'))
        tmpl = 'form_bare.html' if flag else 'base.html'
        return dict(form_base_template=tmpl, rendering_for_dialog=flag)

    if app.debug:
        import IPython

        @app.cli.command('ishell')
        def ishell():
            IPython.start_ipython(argv=[])

    return app
