"""
Django settings for brahms project.

Generated by 'django-admin startproject' using Django 2.2.24.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from dj_database_url import config as db_url_env
import django_cache_url


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# AWS creds may be used for S3 and/or Elasticsearch
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
AWS_REGION = os.getenv('AWS_REGION', '')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# Apps specific for this project go here.
LOCAL_APPS = [
    'vue_app',
    'brahms.home',
    'brahms.search',
]

# Application definition

INSTALLED_APPS = LOCAL_APPS + [
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.settings',
    'wagtail_localize',
    'wagtail.locales',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'brahms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'brahms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': db_url_env('DATABASE_URL', default='postgres:///harbin'),
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
WAGTAIL_I18N_ENABLED = True

USE_L10N = True

USE_TZ = True

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
    ('ru', 'Russian'),
    # ('zh', 'Chinese'),
    # ('ko', 'Korean'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/2.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')
STATIC_URL = '/collectstatic/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = "brahms"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'

# configure CACHES from CACHE_URL environment variable (defaults to locmem if no CACHE_URL is set)
CACHES = {'default': django_cache_url.config()}


# Configure Elasticsearch, if present in os.environ
ELASTICSEARCH_ENDPOINT = os.getenv('ELASTICSEARCH_ENDPOINT', '')

if ELASTICSEARCH_ENDPOINT:
    from elasticsearch import RequestsHttpConnection
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'wagtail.search.backends.elasticsearch5',
            'HOSTS': [{
                'host': ELASTICSEARCH_ENDPOINT,
                'port': int(os.getenv('ELASTICSEARCH_PORT', '9200')),
                'use_ssl': os.getenv('ELASTICSEARCH_USE_SSL', 'off') == 'on',
                'verify_certs': os.getenv('ELASTICSEARCH_VERIFY_CERTS', 'off') == 'on',
            }],
            'OPTIONS': {
                'connection_class': RequestsHttpConnection,
            },
        }
    }

    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        from aws_requests_auth.aws_auth import AWSRequestsAuth
        WAGTAILSEARCH_BACKENDS['default']['HOSTS'][0]['http_auth'] = AWSRequestsAuth(
            aws_access_key=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_token=os.getenv('AWS_SESSION_TOKEN', ''),
            aws_host=ELASTICSEARCH_ENDPOINT,
            aws_region=AWS_REGION,
            aws_service='es',
        )
    elif AWS_REGION:
        # No API keys in the environ, so attempt to discover them with Boto instead, per:
        # http://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials
        # This may be useful if your credentials are obtained via EC2 instance meta data.
        from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
        WAGTAILSEARCH_BACKENDS['default']['HOSTS'][0]['http_auth'] = BotoAWSRequestsAuth(
            aws_host=ELASTICSEARCH_ENDPOINT,
            aws_region=AWS_REGION,
            aws_service='es',
        )
