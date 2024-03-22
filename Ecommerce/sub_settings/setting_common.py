from pathlib import Path
from dotenv import dotenv_values, load_dotenv
import os
import dj_database_url

env = dotenv_values("../../.env")


SECRET_KEY = env.get("SECRET_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# print(env.get("DEBUG_MODE"))
print("\n \n INSIDE SETTINGS \n \n")
# Determine the directory containing settings.py
# Determine the root directory
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# Load the .env file located in the root directory
load_dotenv(dotenv_path=os.path.join(root_dir, '.env'))

# List all items in the root directory
items = os.listdir(root_dir)

# Print the list of items
for item in items:
    print(item)

my_variable = os.getenv('SECRET_KEY')
print(f"SECRET_KEY: {my_variable}")

print(env)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', "192.168.43.150"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",

    # All app services
    "applications.authentication",
    "applications.product",
    "applications.purchase",
]

"""
Rest framework settings
"""
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "PAGE_SIZE": 10,
}

"""
Swagger settings
"""
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}

list1 = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if env.get("DEBUG_MODE") != "True":
    list1.append('whitenoise.middleware.WhiteNoiseMiddleware')


MIDDLEWARE = list1 + MIDDLEWARE

ROOT_URLCONF = 'Ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ecommerce.wsgi.application'

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

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Custom user model referenced inside setting
AUTH_USER_MODEL = "authentication.CustomUser"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ""
STATICFILES_STORAGE = ""
if env.get("DEBUG_MODE") == "True":
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# Media url to store file or images or even document, etc,....
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    "127.0.0.1",
]

# File management 5MO
DATA_UPLOAD_MAX_MEMORY_SIZE = 5621440

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     "http://192.168.43.215",
#     # "http://localhost:3000",
# ]

