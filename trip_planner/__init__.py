from flask import Flask, render_template, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

from .auth import auth  # noqa: E402
from .models import User  # noqa: E402


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='LC!4.0tmi06@0J~YXiqjHVkCU3x1vDhA',
        SQLALCHEMY_DATABASE_URI='postgresql:///trip_planner'
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.before_request
    def get_user():
        try:
            user_id = session['user_id']
            if user_id is None:
                return
            g.user = User.query.filter_by(id=user_id).first()
        except KeyError:
            return

    @app.route("/")
    def root():
        return render_template('root.html')

    app.register_blueprint(auth)

    if app.env == 'development':
        import IPython

        @app.cli.command('ishell')
        def ishell():
            IPython.start_ipython(argv=[])

    return app
