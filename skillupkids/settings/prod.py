import os
from .settings import *

SECRET_KEY = 'django-insecure-shst$+ksll6x&wmyrsy69%7r%(sd(o=9g2lw61d_16xkdv*n-)'
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