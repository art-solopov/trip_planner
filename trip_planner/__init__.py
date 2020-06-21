import os
import os.path

from flask import Flask, render_template, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from wtforms import Field
from wtforms import widgets as ww
from markupsafe import Markup


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

    @app.template_test('hidden_field')
    def is_hidden_field(field: Field) -> bool:
        return getattr(field.widget, 'input_type', '') == 'hidden'

    @app.template_filter('mui_field_class')
    def field_class(field: Field) -> str:
        widget = field.widget
        if isinstance(widget, ww.Select):
            return 'mui-select'
        if isinstance(widget, ww.TextArea):
            return 'mui-textfield'
        if widget.input_type in ('textarea', 'text', 'password'):
            return 'mui-textfield'

        return ''

    @app.context_processor
    def inject_icon_defs():
        with app.open_resource(f'static/icons/icon-defs.svg', 'r') as f:
            return {'icon_defs': Markup(f.read())}

    if app.env == 'development':
        import IPython

        @app.cli.command('ishell')
        def ishell():
            IPython.start_ipython(argv=[])

    return app
