"""
Django settings for wellregistry project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import ast
import logging
import os
import sys

from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    from .local_settings import SECRET_KEY
except ImportError:
    SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEBUG' in os.environ

logging.basicConfig(format="%(asctime)s [%(levelname)-8s] %(message)s",
                    level=logging.DEBUG if DEBUG else logging.INFO)

allowed_hosts = os.getenv('ALLOWED_HOSTS', '[]')

try:
    ALLOWED_HOSTS = ast.literal_eval(allowed_hosts)
    if not isinstance(ALLOWED_HOSTS, list):
        raise TypeError('ALLOWED_HOSTS must be a list.')
except ValueError:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'postgres',
    'registry',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allow_cidr.middleware.AllowCIDRMiddleware'
]

ROOT_URLCONF = 'wellregistry.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'basic': {
            'format': '%(asctime)s [%(levelname)-8s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'basic'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO'
    }
}

# use the AllowCIDRMiddleware to support a CIDR range to ensure that an AWS health check can work
CIDR_RANGES = os.getenv('CIDR_RANGES', None)
if CIDR_RANGES is not None:
    CIDR_RANGES = ast.literal_eval(CIDR_RANGES)
    ALLOWED_CIDR_NETS = CIDR_RANGES

WSGI_APPLICATION = 'wellregistry.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
ENVIRONMENT = {
    'DATABASE_NAME': os.getenv('DATABASE_NAME', 'postgres'),
    'DATABASE_HOST': os.getenv('DATABASE_HOST'),
    'DATABASE_PORT': os.getenv('DATABASE_PORT', default='5432'),
    'DATABASE_USERNAME': os.getenv('DATABASE_USERNAME', 'postgres'),  # not necessary the same name
    'DATABASE_PASSWORD': os.getenv('DATABASE_PASSWORD'),

    'APP_DATABASE_NAME': os.getenv('APP_DATABASE_NAME'),
    'APP_DB_OWNER_USERNAME': os.getenv('APP_DB_OWNER_USERNAME'),
    'APP_DB_OWNER_PASSWORD': os.getenv('APP_DB_OWNER_PASSWORD'),

    'APP_SCHEMA_NAME': os.getenv('APP_SCHEMA_NAME', 'public'),
    'APP_SCHEMA_OWNER_USERNAME': os.getenv('APP_SCHEMA_OWNER_USERNAME'),
    'APP_SCHEMA_OWNER_PASSWORD': os.getenv('APP_SCHEMA_OWNER_PASSWORD'),

    'APP_ADMIN_USERNAME': os.getenv('APP_ADMIN_USERNAME'),
    'APP_ADMIN_PASSWORD': os.getenv('APP_ADMIN_PASSWORD'),
    'APP_CLIENT_USERNAME': os.getenv('APP_CLIENT_USERNAME'),
    'APP_CLIENT_PASSWORD': os.getenv('APP_CLIENT_PASSWORD'),
}

# short alias
env = ENVIRONMENT

if 'test' in sys.argv:
    DATABASES = {
        'default': {  # used for integration tests
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }
elif 'migrate' in sys.argv:
    DATABASES = {
        # Because the default connection alias is not a full dba,
        # this requires this command 'python manager.py migrate --database=postgres'
        'default': {  # used for Django migration in app database
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env['APP_DATABASE_NAME'],
            'HOST': env['DATABASE_HOST'],
            'PORT': env['DATABASE_PORT'],
            'USER': env['APP_DB_OWNER_USERNAME'],
            'PASSWORD': env['APP_DB_OWNER_PASSWORD'],
        },
        'postgres': {  # only needed for Django migration 0001_create_db_users
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env['DATABASE_NAME'],
            'HOST': env['DATABASE_HOST'],
            'PORT': env['DATABASE_PORT'],
            'USER': env['DATABASE_USERNAME'],
            'PASSWORD': env['DATABASE_PASSWORD'],
        },
    }
else:
    DATABASES = {
        # this connection will be for users and will connect to the cloud database
        # they will have CRUD on Registry only and select on lookup tables
        'default': {  # the connection for the client users with the minimum actions
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env['APP_DATABASE_NAME'],  # 'postgis_25_test',
            'HOST': env['DATABASE_HOST'],  # 'localhost',
            'PORT': env['DATABASE_PORT'],  # '5432',
            'USER': env['APP_CLIENT_USERNAME'],  # 'app_user',
            'PASSWORD': env['APP_CLIENT_PASSWORD'],  # 'app_pwd',
        },
        'django_admin': {  # used for Django admin actions
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env['APP_DATABASE_NAME'],
            'HOST': env['DATABASE_HOST'],
            'PORT': env['DATABASE_PORT'],
            'USER': env['APP_ADMIN_USERNAME'],
            'PASSWORD': env['APP_ADMIN_PASSWORD'],
        },
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
