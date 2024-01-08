import os
from .settings import *
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = 'django-insecure-shst$+ksll6x&wmyrsy69%7r%(sd(o=9g2lw61d_16xkdv*n-)'
DEBUG = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_URL='/media/'
MEDIA_ROOT = '/var/task/media'

ALLOWED_HOSTS = ['*', '.vercel.app', '.now.sh',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'URL': os.getenv('PGURL'),
        'NAME': os.getenv('PGDATABASE'),
        'USER': os.getenv('PGUSER'),
        'PASSWORD': os.getenv('PGPASSWORD'),
        'HOST': os.getenv('PGHOST'),
        'PORT': os.getenv('PGPORT'),
    }
}