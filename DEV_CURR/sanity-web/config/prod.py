"""
setting for production environment
"""
import os
from .commonsettings import *


SECRET_KEY = os.environ['SECRET_KEY']

DB_NAME = os.environ['DB_NAME']
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'HOST': 'sjc-dbpl-mysql5.cisco.com',
        'PORT': '3306',
    }
}
