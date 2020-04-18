accesslog = '-'
errorlog = 'log/error.log'
preload_app = True
pidfile = 'tmp/gunicorn.pid'
workers = 3

bind = ['unix:tmp/gunicorn.sock']
