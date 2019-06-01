from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# SSL/HTTPS
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# logging
LOGGING = {
    'version': 1,
    'diable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '{message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        'django': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}
