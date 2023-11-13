import os
from .settings import *

SECRET_KEY = 'django-insecure-shst$+ksll6x&wmyrsy69%7r%(sd(o=9g2lw61d_16xkdv*n-)'
DEBUG = True
STATIC_ROOT = os.path.join(BASE_DIR, 'app/static')

ALLOWED_HOSTS = ['*']