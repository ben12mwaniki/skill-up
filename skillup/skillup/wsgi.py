"""
WSGI config for skillup project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillup.settings')

# application = get_wsgi_application()

# Use WhiteNoise to serve static files

application = WhiteNoise(get_wsgi_application())

