import os

from .settings import BASE_DIR, ALLOWED_HOSTS

DEBUG = True

ALLOWED_HOSTS.append('127.0.0.1')
ALLOWED_HOSTS.append('localhost')

# Django debug toolbar
INTERNAL_IPS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'NAME': 'level_up',
        'ENGINE': 'django.db.backends.postgresql'
    },
    'levelUp': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = "levelup/static/images/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "levelup/static/"),
]
