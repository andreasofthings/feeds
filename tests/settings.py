from defaults import *

# Database for travis
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'myapp_test',
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
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    }
}
