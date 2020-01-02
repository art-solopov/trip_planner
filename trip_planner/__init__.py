from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


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

    @app.route("/")
    def root():
        return "Hello world!"

    return app
