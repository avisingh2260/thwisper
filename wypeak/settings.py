"""
Django settings for wypeak project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
from django.conf.global_settings import SESSION_ENGINE

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&ta_q1kci^@b(4f#9%zgmu&yaoynt!-1qudq(-1w&#p(+_osb_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wypeak'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'wypeak.urls'

WSGI_APPLICATION = 'wypeak.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
#DATABASES = {'default': dj_database_url.config(default='mongodb://IbmCloud_79fd61ag_icneu9c7_t8dts3t2:lqAO30NIWXej-fSmhzHwVwT3KK0-O39B@ds027708.mongolab.com:27708/IbmCloud_79fd61ag_icneu9c7')}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#MONGO_URI = "mongodb://IbmCloud_79fd61ag_icneu9c7_t8dts3t2:lqAO30NIWXej-fSmhzHwVwT3KK0-O39B@ds027708.mongolab.com:27708/IbmCloud_79fd61ag_icneu9c7"
#MONGO_URI = "mongodb://IbmCloud_ve6fs9jj_8q5i6ipc_mign1psb:hSAFfrfd-TRk8n2e43aUagnuv59vbULh@ds035237.mongolab.com:35237/IbmCloud_ve6fs9jj_8q5i6ipc"
'''
DATABASES = {
      "default": {
        "name": "MongoLab-b9",
        "label": "mongolab",
        "plan": "sandbox",
        "credentials": {
          "uri": "mongodb://IbmCloud_79fd61ag_icneu9c7_t8dts3t2:lqAO30NIWXej-fSmhzHwVwT3KK0-O39B@ds027708.mongolab.com:27708/IbmCloud_79fd61ag_icneu9c7"
        }
      }
}
'''
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
TEMPLATE_DIRS = (
    "templates",
    os.path.join(BASE_DIR,'templates')
  #  "/home/html/templates/default",
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
   os.path.join(BASE_DIR,'static'),
)
