"""
WSGI config for turnthepage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

activate_this = '{0}/venv/bin/activate_this.py'.format(BASE_DIR)
with open(activate_this) as f:
    exec(f.read(), dict(__file__=activate_this))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings.product')

application = get_wsgi_application()

