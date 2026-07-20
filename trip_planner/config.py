from os import getenv


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URI')
    SECRETS_PATH = 'secrets.toml'


class Development(Config):
    SECRET_KEY = 'LC!4.0tmi06@0J~YXiqjHVkCU3x1vDhA'
    SQLALCHEMY_ECHO = True
    # Don't let the client cache static files:
    SEND_FILE_MAX_AGE_DEFAULT = 0


class Production(Config):
    SESSION_COOKIE_SECURE = True
