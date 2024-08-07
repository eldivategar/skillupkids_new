import os
from .settings import *

SECRET_KEY = 'django-insecure-shst$+ksll6x&wmyrsy69%7r%(sd(o=9g2lw61d_16xkdv*n-)'
DEBUG = True

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'app/static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_URL='/media/'
# MEDIA_ROOT = BASE_DIR /'media'

ALLOWED_HOSTS = ['*']

# connect with sqlite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MIDTRANS_CLIENT_KEY = os.getenv('MIDTRANS_CLIENT_KEY')
MIDTRANS_SERVER_KEY = os.getenv('MIDTRANS_SERVER_KEY')
SNAP_JS_URL = os.getenv('SNAP_JS_URL')