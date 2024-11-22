"""ASGI config for the Kaartdijin Boodja project.

It exposes the ASGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""


# Standard
import os

# Third-Party
from django.core import asgi


# Set Django settings environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "govapp.settings")

# Create ASGI handler
application = asgi.get_asgi_application()
