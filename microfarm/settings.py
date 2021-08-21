import os
from pathlib import Path
from decouple import config
import locale
from datetime import timedelta

config.encoding = locale.getpreferredencoding(False)

BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = config("ENVIRONMENT", default="development")
SECRET_KEY = config("SECRET_KEY", default=None)
if not SECRET_KEY:
    print(
        '"SECRET_KEY" not configured in environment! Configure it, and re-run the runserver command.'
    )
    exit(0)

DEBUG = ENVIRONMENT == "development"

if ENVIRONMENT == "production":
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # required for authentication
    "django.contrib.sites",
    # restframework apps
    "rest_framework",
    "rest_framework.authtoken",
    # dj-rest-auth apps
    "dj_rest_auth",
    "dj_rest_auth.registration",
    # all-auth apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.twitter",
    # celery apps
    "django_celery_beat",
    # django-microfarm apps
    "commons.apps.CommonsConfig",
    "market_garden.apps.MarketGardenConfig",
    "market_garden.todo.apps.TodoConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "microfarm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "microfarm.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME", default="postgres"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # "rest_framework.authentication.BasicAuthentication",
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

AUTHENTICATION_BACKENDS = {
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
}

REST_USE_JWT = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("ACCESS_TOKEN_LIFETIME", default=5, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("REFRESH_TOKEN_LIFETIME", default=1, cast=int)
    ),
    "ROTATE_REFRESH_TOKENS": config("ROTATE_REFRESH_TOKENS", default=True, cast=bool),
    "BLACKLIST_AFTER_ROTATION": config(
        "BLACKLIST_AFTER_ROTATION", default=True, cast=bool
    ),
    "UPDATE_LAST_LOGIN": config("UPDATE_LAST_LOGIN", default=False, cast=bool),
    "ALGORITHM": config("ALGORITHM", default="HS256", cast=str),
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": config("VERIFYING_KEY", default=None),
    "AUDIENCE": config("AUDIENCE", default=None),
    "ISSUER": config("ISSUER", default=None),
    "JWK_URL": config("JWK_URL", default=None),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(
        minutes=config("SLIDING_TOKEN_LIFETIME", default=5, cast=int)
    ),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(
        days=config("SLIDING_TOKEN_REFRESH_LIFETIME", default=1, cast=int)
    ),
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "static_files")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = config("SITE_ID", default=1, cast=int)

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="none")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="none")

ACCOUNT_EMAIL_REQUIRED = config("ACCOUNT_EMAIL_REQUIRED", default=True)
ACCOUNT_EMAIL_VERIFICATION = config("ACCOUNT_EMAIL_VERIFICATION", default="none")
ACCOUNT_AUTHENTICATION_METHOD = config(
    "ACCOUNT_AUTHENTICATION_METHOD", default="username_email"
)


# Weather and Forecast API KEYS

WEATHER_API_KEY = config("WEATHER_API_KEY", default=None)
FORECAST_API_KEY = config("FORECAST_API_KEY", default=None)

# Timezone API KEY

TIMEZONE_API_KEY = config("TIMEZONE_API_KEY", default=None)
