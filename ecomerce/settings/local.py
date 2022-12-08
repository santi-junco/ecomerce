from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

URL_BASE = parser.get('ambiente','host')
PORT_BACK = parser.get('ambiente','port_back')
PORT_FRONT= parser.get('ambiente','port_front')

PATH_ERROR = 'error-redireccion'
PATH_ERROR_VERIF = 'error-verificacion'
PATH_URL_REDIRECT = 'auth/login'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parser.get('default','name'),
        'USER':  parser.get('default','user'),
        'PASSWORD':  parser.get('default','password'),
        'HOST': parser.get('default','host'),
        'PORT': parser.get('default','port')
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = parser.get('email','user')
EMAIL_HOST_PASSWORD = parser.get('email','password')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
