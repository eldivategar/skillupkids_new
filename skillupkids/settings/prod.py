import os
from .settings import *
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = 'django-insecure-shst$+ksll6x&wmyrsy69%7r%(sd(o=9g2lw61d_16xkdv*n-)'
DEBUG = False

STATIC_URL = 'https://sukcdn.netlify.app/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

MEDIA_URL='/media/'
# MEDIA_ROOT = '/var/task/media'

ALLOWED_HOSTS = ['*', '.vercel.app', '.now.sh',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'URL': os.getenv('POSTGRES_URL'),
        'NAME': os.getenv('POSTGRES_DATABASE'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        # 'PORT': os.getenv('PGPORT'),
    }
}