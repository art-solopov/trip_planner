class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRETS_PATH = 'secrets.json'


class Development(Config):
    SECRET_KEY = 'LC!4.0tmi06@0J~YXiqjHVkCU3x1vDhA'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///trip_planner'
    SQLALCHEMY_ECHO = True
    # Don't let the client cache static files:
    SEND_FILE_MAX_AGE_DEFAULT = 0


class Production(Config):
    SESSION_COOKIE_SECURE = True
