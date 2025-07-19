from os import getenv

accesslog = '-'
errorlog = 'log/error.log'
preload_app = True
pidfile = 'tmp/gunicorn.pid'
workers = int(getenv('GUNICORN_CONCURRENCY', '3'))

bind = ['unix:tmp/gunicorn.sock']
