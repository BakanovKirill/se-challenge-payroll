from __future__ import unicode_literals, absolute_import
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'paydb_test',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, '_sent_mails')

DEBUG = True

SETTINGS_TITLE = 'test'
