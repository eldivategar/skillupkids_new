import os
from .settings import *

SECRET_KEY = 'django-insecure-shst$+ksll6x&wmyrsy69%7r%(sd(o=9g2lw61d_16xkdv*n-)'
DEBUG = False
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', '.now.sh', 'skillupkids.id', 'www.skillupkids.id']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'URL': 'postgresql://postgres:B21AfcFDBaAaFFGAgaeF53Aa61-egGf3@roundhouse.proxy.rlwy.net:38061/railway',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'B21AfcFDBaAaFFGAgaeF53Aa61-egGf3',
        'HOST': 'roundhouse.proxy.rlwy.net',
        'PORT': 38061,
    }
}