# Local
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.rq import RqIntegration

# Core
ALLOWED_HOSTS = [
    '.barberscore.com',
    '.herokuapp.com',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
SECURE_SSL_REDIRECT = True

# Sentry
sentry_sdk.init(
    dsn=get_env_variable("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
        RqIntegration(),
    ],
    send_default_pii=True,
    environment=get_env_variable("HEROKU_APP_NAME"),
)

# Databases
DATABASES = {
    'default': dj_database_url.parse(
        get_env_variable("DATABASE_URL"),
        conn_max_age=600,
    ),
    'source_db': dj_database_url.parse(
        get_env_variable("BHS_DATABASE_URL"),
        conn_max_age=600,
    ),
}

DATABASE_ROUTERS = [
    'routers.SourceRouter',
]

# Search
# ALGOLIA['AUTO_INDEXING'] = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'django': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'api': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'importer': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'updater': {
            'handlers': [
                'console',
            ],
            'level': 'INFO',
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': [
                'console'
            ],
            'propagate': False,
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
}
