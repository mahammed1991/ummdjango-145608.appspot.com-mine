"""
Django settings for umm_tool project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from djangae.settings_base import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!zi17==vxh)n@lrbdz_d3yc(#y#as-3qt4=u+^uawsa&rxga59'

#AUTH_USER_MODEL = 'djangae.GaeDatastoreUser'
# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('SETTINGS_MODE') == 'prod':
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    #'djangae.contrib.gauth',
    'djangae',
    'django.contrib.admin',
    'django.contrib.auth',
    'djangae.contrib.gauth.sql',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'umm_app',
    'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'djangae.contrib.security.middleware.AppEngineSecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'djangae.contrib.gauth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'djangae.contrib.gauth.backends.AppEngineUserAPI',
)

ROOT_URLCONF = 'umm_tool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'umm_tool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine'):
    # Running on production App Engine, so use a Google Cloud SQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '/cloudsql/ummdjango-145608:apollo',
            'NAME': 'umm_tool',
            'USER': 'root',
        }
    }
elif os.getenv('SETTINGS_MODE') == 'prod':
    # Running in production, but want to access the Google Cloud SQL instance in production.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': '173.194.243.38',
            'NAME': 'umm_tool',
            'USER': 'test',
            'PASSWORD': 'test',
            #'OPTIONS':  {
            #    'ssl': {
            #        'ca': 'server-ca.pem',
            #        'cert': 'client-cert.pem',
            #        'key': 'client-key.pem'
            #    }
            #}
        }
    }
else:
    # Running in development, so use a local MySQL database.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'umm_tool',
            'USER': 'root',
            'PASSWORD': 'root',
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# STATIC_ROOT = 'static'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)


TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
   'social.backends.google.GoogleOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "50509765568-3q8cbe5vng1dt6ud5l7dfvqpg1bi76jh.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "kdKcI8PqSqb9ic_m_de6QbTt"

LOGIN_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/auth/error'

# Social Auth error handling
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = LOGIN_URL
SOCIAL_AUTH_BACKEND_ERROR_URL = LOGIN_URL

# Use email as username for user acccounts
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True

# list of domains allowed
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['regalix-inc.com', 'google.com']
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = ['']

SOCIAL_AUTH_RAISE_EXCEPTIONS = True

SOCIAL_AUTH_SESSION_EXPIRATION = False

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'umm_app.views.check_email',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

if os.getenv('SETTINGS_MODE') == 'prod':
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False