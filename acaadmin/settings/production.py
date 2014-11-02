"""Django settings for the acaadmin project."""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE_DIR = os.path.abspath(os.path.join(SITE_ROOT, '..'))

SECRET_KEY = os.environ['SECRET_KEY']

# Application definition

ALLOWED_HOSTS = ['.herokuapp.com']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'bootstrap3',
    'songs',
    'schedule',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOpenId',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates'),
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
      'django.template.loaders.filesystem.Loader',
      'django.template.loaders.app_directories.Loader',
    )),
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ROOT_URLCONF = 'acaadmin.urls'

WSGI_APPLICATION = 'acaadmin.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(),
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files stuff

STATICFILES_STORAGE = 'require_s3.storage.OptimizedCachedStaticFilesStorage'
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_AUTO_CREATE_BUCKET = True
AWS_HEADERS = {
    'Cache-Control': 'public, max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True
AWS_REDUCED_REDUNDANCY = False
AWS_IS_GZIPPED = False
STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME

STATICFILES_DIRS = (
    os.path.join(SITE_ROOT, 'static'),
)

# Cache stuff

CACHE_MIDDLEWARE_KEY_PREFIX = 'acaadmin'

CACHES = {
    'default': {
      'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    # Long cache timeout for staticfiles, since this is used heavily
    # by the optimizing storage.
    'staticfiles': {
      'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
      'TIMEOUT': 60 * 60 * 24 * 365,
      'LOCATION': 'staticfiles',
    },
}

# Logging config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
      'console': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
      },
    },
    'loggers': {
      'django': {
        'handlers': ['console'],
      },
    },
}

LOGIN_URL = '/login/google'
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/error'
