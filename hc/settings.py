"""
Django settings for hc project.
Generated by 'django-admin startproject' using Django 1.8.2.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import warnings
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOST = "localhost"
SECRET_KEY = "---"
DEBUG = True
ALLOWED_HOSTS = []
DEFAULT_FROM_EMAIL = 'healthchecks@example.org'
USE_PAYMENTS = False


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',
    'djmail',

    'hc.accounts',
    'hc.api',
    'hc.front',
    'hc.payments'
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'hc.accounts.middleware.TeamAccessMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'hc.accounts.backends.EmailBackend',
    'hc.accounts.backends.ProfileBackend'
)

ROOT_URLCONF = 'hc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'hc.payments.context_processors.payments'
            ],
        },
    },
]

WSGI_APPLICATION = 'hc.wsgi.application'
TEST_RUNNER = 'hc.api.tests.CustomRunner'


# Default database engine is SQLite. So one can just check out code,
# install requirements.txt and do manage.py runserver and it works
DATABASES = {
    'default': dj_database_url.config()
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME':   './hc.sqlite',
#     }
# }

# You can switch database engine to postgres or mysql using environment
# variable 'DB'. Travis CI does this.
if os.environ.get("DB") == "postgres":
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     'hc',
            'USER':     'postgres',
            'TEST': {'CHARSET': 'UTF8'}
        }
    }

if os.environ.get("DB") == "mysql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'USER':     'root',
            'NAME':     'hc',
            'TEST': {'CHARSET': 'UTF8'}
        }
    }

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ROOT = "https://job-run-fast.herokuapp.com"
PING_ENDPOINT = SITE_ROOT + "/ping/"
PING_EMAIL_DOMAIN = HOST
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'static-collected')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
COMPRESS_OFFLINE = True

EMAIL_BACKEND = "djmail.backends.default.EmailBackend"

# Slack integration -- override these in local_settings
SLACK_CLIENT_ID = None
SLACK_CLIENT_SECRET = None

# Pushover integration -- override these in local_settings
PUSHOVER_API_TOKEN = None
PUSHOVER_SUBSCRIPTION_URL = None
PUSHOVER_EMERGENCY_RETRY_DELAY = 300
PUSHOVER_EMERGENCY_EXPIRATION = 86400

# Pushbullet integration -- override these in local_settings
PUSHBULLET_CLIENT_ID = None
PUSHBULLET_CLIENT_SECRET = None

if os.path.exists(os.path.join(BASE_DIR, "hc/local_settings.py")):
    from .local_settings import *
else:
    warnings.warn("local_settings.py not found, using defaults")

# smtp server config
DJMAIL_REAL_BACKEND = 'djmail.backends.async.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')  # your email
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # your password
EMAIL_USE_TLS = True