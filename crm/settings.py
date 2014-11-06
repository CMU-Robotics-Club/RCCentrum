import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Override These
# =========================

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

GOOGLE_API_KEY = ''

# The Project ID's who have permission to set a user's RFID tag
RFID_POST_PROJECT_IDS = []

# The Project ID's who have permission to send emails as well as an array of robouser IDs project can send to(None all IDs, [] no IDs)
#EMAIL_POST_PROJECT_IDS = {1:[2, 40, 52]}
EMAIL_POST_PROJECT_IDS = {}

# ==========================

DEBUG = True
TEMPLATE_DEBUG = DEBUG

AUTH_PROFILE_MODULE = 'robocrm.RoboUser'

ADMINS = (
    ('Brent Strysko', 'bstrysko@andrew.cmu.edu'),
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'crm',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

GOOGLE_CALENDAR_ID = "85bf0h78fidsgkkgmkktrqasm8%40group.calendar.google.com"

PROJECT_ACTIVE_SECONDS = 10

CHANNEL_ACTIVE_TIME_DELTA = timedelta(minutes=5)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/crm/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader',(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ),
    ),
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'crm.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'crm.wsgi.application'

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATE_DIRS = (
    TEMPLATE_DIR,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'robocrm',
    'officers',
    'projects',
    'api',
    'webcams',
    'channels',
    'ordered_flatpages',
    'resources',
    'sponsors',
    'social_media',
    'links',
    'posters',
    'tshirts',
    'quotetron',
    'tinymce',
    'rest_framework',
    'ordered_model',
    'suit',
    'django.contrib.admin',
    'password_reset',
    'easy_thumbnails',

    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'theme_advanced_buttons3_add': 'code',
    'valid_elements': '*[*]',
    'convert_urls' : False,
    'relative_urls' : False,
    'forced_root_block' : False,
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'api.authentication.RCAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'EXCEPTION_HANDLER': 'api.exception_handler.api_exception_handler',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_csv.renderers.CSVRenderer',
    ),
}

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

THUMBNAIL_ALIASES = {
    '': {
        'poster_index': {
            # Aspect Ratio 1.6425855
            'size': (821, 500),
            'crop': True
        },
        'poster_admin': {
            # Aspect Ratio 1.6425855
            'size': (328, 200),
            'crop': True
        }
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'django_file': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '{}/logs/django_log.log'.format(BASE_DIR),
            'maxBytes': 1024*1024*50, # 50 MB
            'backupCount': 5,
            'formatter':'default',
        },
        'api_file': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '{}/logs/api_log.log'.format(BASE_DIR),
            'maxBytes': 1024*1024*50, # 50 MB
            'backupCount': 5,
            'formatter':'default',
        },
        'apps_file': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '{}/logs/apps_log.log'.format(BASE_DIR),
            'maxBytes': 1024*1024*50, # 50 MB
            'backupCount': 5,
            'formatter':'default',
        },   
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api': {
            'handlers': ['api_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'channels': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'crm': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'links': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'officers': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'ordered_flatpages': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'projects': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'resources': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'robocrm': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'social_media': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'sponsors': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'webcams': {
            'handlers': ['apps_file', ],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

try:
    from .local_settings import *
except ImportError:
    pass
