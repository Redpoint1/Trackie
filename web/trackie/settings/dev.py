""" Development configuration for Django """

from .common import *  # pylint: disable=wildcard-import,unused-wildcard-import
DEBUG = True

INSTALLED_APPS += (
    'debug_toolbar',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

DEBUG_TOOLBAR_PATCH_SETTINGS = True
SHOW_TOOLBAR_CALLBACK = True
