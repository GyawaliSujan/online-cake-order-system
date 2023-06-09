"""
Django settings for mrcake project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


BASE_DIR = environ.Path(__file__) - 3

env = environ.Env(DEBUG=(bool, False),) # set default values and casting
environ.Env.read_env(env_file=BASE_DIR('.env'))
BASE_DIR = str(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kek9ch3dh^uf04skj_)d7vcn=y#imlcfx(1pi*s!cw2e#inhz6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("HOST", default=["*"])

# Application definition

CORE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
]

LOCAL_APPS = [
    'product',
    'registration',
    'contact',
    'review',
    'payment',
]

THIRD_PARTY_APPS = [
    'debug_toolbar',
    'django_extensions',
    'rest_framework',
    'bootstrap3',
    'django_inlinecss',
    'paypal.standard.ipn',
    'compressor',
    'sorl.thumbnail'
]

INSTALLED_APPS = CORE_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'mrcake.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mrcake.context_processors.settings_data'
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
)

WSGI_APPLICATION = 'mrcake.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {"default": env.db()}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email Settings to send email
EMAIL_USE_TLS = True
EMAIL_HOST = env.str("EMAIL_HOST", "")
EMAIL_PORT = 587
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


SITE_ID = 1

ADMINS = (('Saurav', 'sp.gharti@gmail.com'))

# allauth settings
INSTALLED_APPS += (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
)

AUTHENTICATION_BACKENDS += (
    "allauth.account.auth_backends.AuthenticationBackend",)

ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_FORMS = {
    'login': 'registration.forms.LoginForm',
    # signup forms defined in views since student/principal signups different
    #'signup': 'registration.forms.SignupForm',
    #'signup': 'student_site.forms.Signup2EnrollForm',
    'reset_password': 'registration.forms.ResetPasswordForm',
    'reset_password_from_key': 'registration.forms.ResetPasswordKeyForm',
}
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_ADAPTER = 'registration.adapter.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'registration.adapter.SocialAccountAdapter'
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = None
SOCIALACCOUNT_PROVIDERS = \
    {
        'google':
            {
                'SCOPE': ['profile', 'email'],
                'AUTH_PARAMS': {'access_type': 'online'}
            },
        'facebook':
            {
                'METHOD': 'oauth2',
                'SCOPE': ['email'],
                'AUTH_PARAMS': {'auth_type': 'https'},
                'FIELDS': [
                    'id',
                    'email',
                    'name',
                    'first_name',
                    'last_name',
                    'verified',
                    'locale',
                    'timezone',
                    'link',
                    'gender',
                    'updated_time'
                ],
                'EXCHANGE_TOKEN': True,
                'VERIFIED_EMAIL': False,
                'VERSION': 'v2.4'
            },


    }

ACCOUNT_ADAPTER = 'registration.adapter.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'registration.adapter.SocialAccountAdapter'


# authentication key Braintree Sandbox mode
BRAINTREE_MERCHANT_ID = env.str("BRAINTREE_MERCHANT_ID", "")
BRAINTREE_PUBLIC_KEY = env.str("BRAINTREE_PUBLIC_KEY", "")
BRAINTREE_PRIVATE_KEY = env.str("BRAINTREE_PRIVATE_KEY", "")

# paypal config
PAYPAL_TEST = DEBUG
PAYPAL_SANDBOX_IMAGE = "https://www.paypalobjects.com/webstatic/en_US/i/btn/png/gold-rect-paypal-44px.png"
PAYPAL_IMAGE = "https://www.paypalobjects.com/webstatic/en_US/i/btn/png/gold-rect-paypal-44px.png"

# THUMBNAIL_FORCE_OVERWRITE = True
THUMBNAIL_DEBUG = False
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# django debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

PAYPAL_EMAIL = env.str("PAYPAL_EMAIL")
PAYPAL_RATE = 90
PHONE_NUMBERS = env.list("PHONE_NUMBERS", [])
CONTACT_EMAIL = env.str("CONTACT_EMAIL", "")
NOTIFICATION_EMAILS = env.list("NOTIFICATION_EMAILS", [])

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

sentry_sdk.init(
    dsn=env.str("SENTRY_DSN"),
    integrations=[DjangoIntegration()]
)