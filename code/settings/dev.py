from __future__ import unicode_literals, absolute_import
from .base import *

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, '_sent_mails')

DEBUG = True
ENABLE_DEBUG_TOOLBAR = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'paydb',
    }
}

ALLOWED_HOSTS += ['*']

if ENABLE_DEBUG_TOOLBAR:
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE
    INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar', ]

SETTINGS_TITLE = 'dev'
