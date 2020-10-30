"""
Django settings for hololink project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'll_6@mme89*o#z##q7s_hh7g+wvs0f%8^_or_z*$c@nbi(#1!7'

# SECURITY WARNING: don't run with debug turned on in production!
from secret.hololink.settings import DEBUG

ALLOWED_HOSTS = ['*']

# django-debug-tool setting
INTERNAL_IPS = [
    '127.0.0.1',
]
'''
def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}
'''

# Application definition

INSTALLED_APPS = [
    # This make it easier to integrate django templates with bootstrap things.
    'tag_lib.apps.TagLibConfig',
    'accounts.apps.AccountsConfig',
    'article.apps.ArticleConfig',
    'project.apps.ProjectConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd parties
    'rest_framework',
    'rest_framework_api_key',
    'widget_tweaks',
    'rest_framework.authtoken',
    'debug_toolbar',

]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', #setup DRF view default pagnation 
    'PAGE_SIZE': 10
}

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # For dynamic languages
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hololink.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'hololink.wsgi.application'

# Define new login validatiion backend
AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

from secret.hololink.settings import (
    DATABASES,
)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

# We disable the most part of AUTH_PASSWORD_VALIDATORS for convinience of users.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# For i18n
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# This limits the set_language view option
LANGUAGES = {
    ('en', ''),
    ('zh-hant', ''),
}

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads/')

MEDIA_URL = '/uploads/'

# build-in auth system

#LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

# SMTP things
SIGNUP_VERIFICATION_EMAIL_TEXT = 'singup_verification_email.txt'
SIGNUP_VERIFICATION_EMAIL_HTML = 'singup_verification_email.html'
EMAIL_VERIFICATION_PAGE_DOMAIN = 'https://hololink.co/'
from secret.hololink.settings import (
    EMAIL_BACKEND,
    EMAIL_HOST,
    EMAIL_USE_TLS,
    EMAIL_PORT,
    EMAIL_HOST_USER,
    EMAIL_HOST_PASSWORD,
    DEFAULT_FROM_EMAIL,
    SERVER_EMAIL,
)
