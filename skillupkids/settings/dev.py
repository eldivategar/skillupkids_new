import os
from .settings import *

SECRET_KEY = 'django-insecure-shst$+ksll6x&wmyrsy69%7r%(sd(o=9g2lw61d_16xkdv*n-)'
DEBUG = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'app/static')
# STATIC_ROOT = 'https://sukcdn.netlify.app/'

MEDIA_URL='/media/'
# MEDIA_ROOT = BASE_DIR /'media'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'skillupkids_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

MIDTRANS_CLIENT_KEY = os.getenv('SB_MIDTRANS_CLIENT_KEY')
MIDTRANS_SERVER_KEY = os.getenv('SB_MIDTRANS_SERVER_KEY')
SNAP_JS_URL = os.getenv('SB_SNAP_JS_URL')