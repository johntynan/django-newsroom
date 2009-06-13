# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import os.path
import pinax

PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
NEWSROOM_ROOT = os.path.abspath(os.path.dirname(__file__)+'/../newsroom_project')
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# tells Pinax to use the default theme
PINAX_THEME = 'default'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
INLINE_DEBUG = DEBUG

# tells Pinax to serve media through django.views.static.serve.
SERVE_MEDIA = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = os.path.join(NEWSROOM_ROOT, "dev.db"),
# Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'US/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "media")

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and override in local_settings.py
SECRET_KEY = '123-90@#LKJ2p*n0e&e=k4j#z2g6p4p1=g=sem6do%ktbrfawnk'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_openid.consumer.SessionConsumer',
    'account.middleware.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'news21_com.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(NEWSROOM_ROOT, "templates",),
    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "misc.context_processors.site_name",
    "misc.context_processors.contact_email",
    "news21_com.context_processors.google_analytics",
)

INSTALLED_APPS = (
    # included
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.markup',

    # external
    #'notification', # must be first
    'django_openid',
    'emailconfirmation',
    #'mailer',
    #'announcements',
    'pagination',
    'timezones',
    'ajax_validation',
    'uni_form',
    #'avatar',
    #'voting',
    #'countries',
    #'tagging',
    'django_inlines',

    # internal (for now)
    'basic_profiles',
    'staticfiles',
    'account',
    'misc',
    'about',
    'tag_app',

    # newsroom apps
    'stories',
    'multimedia',
    #'aggregator',
    #'core',
    #'utils',
    'promos',
    'topics',
    'videos',
    'photos',
)

PROMO_MODERATORS = (
    # ('Your Name', 'your_email@domain.com'),
)

DEFAULT_FROM_EMAIL = 'webmaster@localhost'

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/%s/" % o.username,
}

AUTH_PROFILE_MODULE = 'basic_profiles.Profile'
NOTIFICATION_LANGUAGE_MODULE = 'account.Account'

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG
CONTACT_EMAIL = "feedback@example.com"
SITE_NAME = "News21"
LOGIN_URL = "/account/login"
LOGIN_REDIRECT_URLNAME = "what_next"


# geotags 
# default key is for localhost/local development
GOOGLE_MAPS_API_KEY = 'ABQIAAAAnfs7bKE82qgb3Zc2YyS-oBT2yXp_ZAY8_ufC3CFXhHIE1NvwkxSySz_REpPq-4WZA27OwgbtyR3VcA'

# Google Analytics
GOOGLE_ANALYTICS_KEY = ''

# django_inlines
INLINES_START_TAG = '<%'
INLINES_END_TAG = '%>'

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
