from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# SSL/HTTPS
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
