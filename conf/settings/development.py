from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost']

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]
