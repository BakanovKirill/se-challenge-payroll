from __future__ import unicode_literals, absolute_import
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'homehero_test',
        'USER': 'hero',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, '_sent_mails')
DEBUG = True
UBER_DEBUG = True

# FB SETTINGS
# FB_APP_ID = '838403169622937'
# FB_APP_SECRET = '8941e4b25e74d2ae9211f351263bd47a'

# Test settings not sending real sms
# TWILIO_ACCOUNT_SID = 'AC3d95d4fce1e7c270d8c8e78456722c9d'
# TWILIO_AUTH_TOKEN = '94409a10b5f1f1d8b6edb4fa18edef5e'
# DEFAULT_TWILIO_FROM_NUMBER = '+15005550006'

CELERY_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

HTTP_METHOD = 'http'
RAVEN_CONFIG = {}
WEBSITE_URL = '%s://localhost:8000' % HTTP_METHOD
LOB_API_KEY = 'test_6fa330ff7277f1b9e7ae9bbf1e6bb4fd56c'

SETTINGS_TITLE = 'test'

# Test keys
RECAPTCHA_PUBLIC_KEY = '6LdKA3AUAAAAABoH6HNhz4rsoZhp01I8TvXrp-ta'
RECAPTCHA_PRIVATE_KEY = '6LdKA3AUAAAAABPinIdz1wohHtzw2nRPePfSoSuj'