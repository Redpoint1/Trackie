""" Development configuration for Django """

from .common import *  # pylint: disable=wildcard-import,unused-wildcard-import
DEBUG = True

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PATCH_SETTINGS = True
SHOW_TOOLBAR_CALLBACK = True

INTERNAL_IPS = [
    "127.0.0.1"
]

CACHES['default']['LOCATION'] = os.path.join(BASE_DIR, "cache", "default")
CACHES['race']['LOCATION'] = os.path.join(BASE_DIR, "cache", "race")
