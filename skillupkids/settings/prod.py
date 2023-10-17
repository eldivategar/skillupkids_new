import os
from .settings import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ['*']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'skillupkids_db',
        'USER': 'root',
        'PASSWORD': 'skillupkidsid',
        'HOST':'localhost',
        'PORT':'3306',
    }
}