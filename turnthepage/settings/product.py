from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# SSL/HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
