import os
import os.path

from flask import Flask, render_template, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask.cli import with_appcontext
from wtforms import Field
from wtforms import widgets as ww
from markupsafe import Markup

from . import assets
from .tailwind import FlashClasses, CommonClasses, FormClasses


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
from .api import api as api_bp  # noqa: E402
from .scripts import scripts as scripts_bp  # noqa: E402
from .models import User  # noqa: E402


def create_app(test_config=None, instance_path=None):
    if instance_path is None:
        env_instance_path = os.getenv('INSTANCE_PATH')
        if env_instance_path:
            instance_path = env_instance_path

    app = Flask(__name__,
                instance_path=instance_path,
                instance_relative_config=True)
    if test_config is not None:
        app.config.from_object(test_config)
    else:
        app.config.from_object(f'trip_planner.config.{app.env.capitalize()}')

    secrets_path = app.config['SECRETS_PATH']
    app.config.from_json(secrets_path)

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
    app.register_blueprint(scripts_bp)

    @app.template_test('hidden_field')
    def is_hidden_field(field: Field) -> bool:
        return getattr(field.widget, 'input_type', '') == 'hidden'

    @app.context_processor
    def inject_icon_defs():
        with app.open_resource(f'static/icons/icon-defs.svg', 'r') as f:
            return {'icon_defs': Markup(f.read())}

    @app.context_processor
    def inject_js_chunks():
        return {
            'chunks': assets.chunks(app),
            'script_tag': assets.script_tag
        }

    @app.context_processor
    def inject_tailwind_vars():
        return {
            'flash_classes': {
                'all': FlashClasses.ALL,
                'categories': FlashClasses.CATEGORIES
            },
            'common_classes': {
                'h1': CommonClasses.TITLE_H1,
                'h1_big': CommonClasses.TITLE_H1_BIG,
                'navbar_text': CommonClasses.NAVBAR_TEXT,
                'navbar_link': CommonClasses.NAVBAR_LINK,
            },
            'form_classes': {
                'input_default': FormClasses.INPUT_DEFAULT
            }
        }

    if app.env == 'development':
        import IPython

        @app.cli.command('ishell')
        def ishell():
            IPython.start_ipython(argv=[])

    return app
