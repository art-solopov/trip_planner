from os import getenv


class FromEnv:
    def __init__(self, key: str, default=None):
        self.key = key
        self.default = default

    def __get__(self, _obj, _t=None):
        return getenv(self.key, self.default)


def from_env(key):
    return FromEnv(key)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAPBOX_APIKEY = from_env('MAPBOX_APIKEY')


class DevelopmentConfig(Config):
    SECRET_KEY = 'LC!4.0tmi06@0J~YXiqjHVkCU3x1vDhA'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///trip_planner'
    # SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    SECRET_KEY = from_env('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = from_env('DATABASE_URI')


ENV_CONFIGS = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}


def get_config(env: str) -> Config:
    return ENV_CONFIGS[env]()
