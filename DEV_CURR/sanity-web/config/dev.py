"""
setting for development environment
"""

from .commonsettings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pc$_zqdbet+*=4fvv3cfm#a5ap%1it+uxku8fz*$a308=yy+h7'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sanity_gui',
        'USER': 'root',
        'PASSWORD': 'iloveDC3.',
        'HOST': 'mysql',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


STATICFILES_DIRS = (
    os.path.join('static_src'),
)
