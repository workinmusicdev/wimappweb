"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

import environ
# settings.py
import os
import firebase_admin
from firebase_admin import credentials
import os
from storages.backends.s3boto3 import S3Boto3Storage

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent





# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pd7(cbqees77gvuo1bl^mdpbiiowe4g*xa2v_e$breh93q=xq_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["app.workinmusic.fr","*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
'allauth',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'allauth.account',
    'allauth.socialaccount',
    'storages',

    "corsheaders",
    'rest_framework',
'dj_rest_auth',
    'dj_rest_auth.registration',




    'import_export',
'djoser',

    "rest_framework_simplejwt.token_blacklist",
    'rest_framework_simplejwt',
    "rest_framework.authtoken",
    'drf_yasg',



    #----
    "accountapp",
    "licenceapp",
    "musicapp",
    "quizzapp"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    "allauth.account.middleware.AccountMiddleware",
'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
       # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
       # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
        'rest_framework_social_oauth2.authentication.SocialAuthentication',

    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=31),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=61),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=31),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
}

WSGI_APPLICATION = 'core.wsgi.application'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if config("mode")=="prod":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    """DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('NAME'),
            'USER': config('USER'),
            'PASSWORD': config('PASSWORD'),
            'HOST': 'db', # Change to your MySQL host if it's not local
            'PORT': config("PORT"),
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_bin',
            'OPTIONS': {
                'use_unicode': True,
                'init_command': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
            },
            # Change to your MySQL port if needed
        }
    }"""
else:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/


LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_ROOT =os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS=[ os.path.join(BASE_DIR, 'statics')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_ALLOW_ALL = True  # or False
#CORS_ALLOW_CREDENTIALS = True
#CORS_ALLOW_ALL_ORIGINS = True
#CORS_ORIGIN_ALLOW = True
AUTH_USER_MODEL = 'accountapp.CustomUser'
CSRF_TRUSTED_ORIGINS = ['https://*.workinmusic.fr','https://*.127.0.0.1',"https://app.workinmusic.fr","http://app.workinmusic.fr"]

#Djsoer
DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": False,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": False,
    "SEND_CONFIRMATION_EMAIL": True,
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_URL": "auth/change-password/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL": "",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": ["http://localhost:3000","https://workinmusic.fr"],
    "SERIALIZERS": {
        "user_create": "accountapp.serializers.CustomUserCreateSerializer",
        "user": "accountapp.serializers.CustomUserUpdateSerializer",
        "current_user": "accountapp.serializers.CustomUserUpdateSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
}
# Auth
AUTHENTICATION_BACKENDS = [
    # Facebook OAuth2

    'social_core.backends.facebook.FacebookOAuth2',

    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',

    "django.contrib.auth.backends.ModelBackend",
    'allauth.account.auth_backends.AuthenticationBackend',



]
#Google
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social_core.backends.apple.AppleIdAuth',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
FACEBOOK_EXTENDED_PERMISSIONS = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'fields': 'id, name, email'}

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'email']
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET =config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]
# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config("SOCIAL_AUTH_FACEBOOK_SECRET")
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.10'
# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from Facebook.
# Email is not sent by default, to get it, you must request the email permission.
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

#Pipeline
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
# Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "wim-ai@workinmusic.fr"
#'contacts@workinmusic.fr'ff
EMAIL_HOST_PASSWORD ="omdqldcfrvhgxbrd"
EMAIL_USE_TLS = True  # Utilisez TLS pour sécuriser la connexion
#-------------------

SOCIAL_AUTH_APPLE_ID_CLIENT= 'com.workinmusic.wimusic'
SOCIAL_AUTH_APPLE_ID_TEAM= config('SOCIAL_AUTH_APPLE_ID_TEAM')               # Your Team ID, ie K2232113
SOCIAL_AUTH_APPLE_ID_KEY= config('SOCIAL_AUTH_APPLE_ID_KEY')                # Your Key ID, ie Y2P99J3N81K
SOCIAL_AUTH_APPLE_ID_SECRET= """
-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgmyF9+Du/EojT0Qpr
SnPOCeb8TZu13NqB0xjvWLwYODGgCgYIKoZIzj0DAQehRANCAAQ/0HDCJPQW/fDV
RpU6xfkc30bDtL6VVDL9PxKcUhMr07Z7WKiTwx5Qf1h5FHbeHL9MKL72W652DugD
pIk4fLQk
-----END PRIVATE KEY-----"""
SOCIAL_AUTH_APPLE_ID_SCOPE = ['email', 'name']
SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME = True


SOCIALACCOUNT_PROVIDERS = {
    'apple': {
        'APP': {
            'client_id': SOCIAL_AUTH_APPLE_ID_CLIENT,
            'secret': {
                'key': SOCIAL_AUTH_APPLE_ID_KEY,
                'team_id': SOCIAL_AUTH_APPLE_ID_TEAM,
                'private_key': SOCIAL_AUTH_APPLE_ID_SECRET,
            },
        }
    }
}

# settings.py

# Import necessary modules

if config("mode")=="prod":
    FIREBASE_ADMIN_CREDENTIAL = os.path.join(BASE_DIR, 'workinmusic-30b37-firebase-adminsdk-h7ihz-8152566065.json')

    cred = credentials.Certificate(FIREBASE_ADMIN_CREDENTIAL)
    firebase_admin.initialize_app(cred)
    # Set the required AWS credentials
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME")

    # Optional: Set custom domain for static and media files
    # AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Set the static and media files locations
    STATICFILES_LOCATION = 'static'
    MEDIAFILES_LOCATION = 'media'

    # Define custom storage classes for static and media files
    class StaticStorage(S3Boto3Storage):
        location = STATICFILES_LOCATION

    class MediaStorage(S3Boto3Storage):
        location = MEDIAFILES_LOCATION
        file_overwrite = False

    # Configure static and media files storage
    STATICFILES_STORAGE = 'core.settings.StaticStorage'
    DEFAULT_FILE_STORAGE = 'core.settings.MediaStorage'

    # Set static and media URLs
    STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{MEDIAFILES_LOCATION}/'
    #------------

# Configure dj-rest-auth and allauth
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = True
LOGIN_REDIRECT_URL = '/'
REST_USE_JWT = True

DRFSO2_URL_NAMESPACE='auth-api'