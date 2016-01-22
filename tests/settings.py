from .defaults import *

# Database for travis
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django.db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Haystack
HAYSTACK_CONNECTIONS = {
    "default": {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': '.',
        'INDEX_NAME': 'haystack',
    }
}
