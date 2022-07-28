"""gunicorn WSGI server configuration."""
from distutils.log import info
from multiprocessing import cpu_count
from os import environ


def max_workers():    
    return cpu_count()*2-1


bind = '0.0.0.0:' + environ.get('PORT', '8002')
max_requests = 1000
workers = max_workers()
accesslog = '/code/logs/gunicorn-access.log'
loglevel = 'info'
errorlog = '/code/logs/gunicorn-error.log'
