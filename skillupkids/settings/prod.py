import os
from .settings import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')