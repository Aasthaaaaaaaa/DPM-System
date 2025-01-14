from pathlib import Path
import firebase_admin
from firebase_admin import credentials, auth, firestore

import os
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
load_dotenv() 

# Fetch the path of the Firebase credentials from environment variables
firebase_cred = os.getenv('FIREBASE_CREDENTIALS_PATH')

if firebase_cred:
    cred = credentials.Certificate(firebase_cred)
    initialize_app(cred)
else:
    raise ValueError("Firebase credentials path is not set!")


# Firebase Authentication Example Usage (verify ID tokens)
def verify_firebase_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        return uid
    except:
        raise ValueError('Invalid token')

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-k^^zshk_o5)$fo=#)--)r%0ra-ygj+&s%5k$4xbyk&+af-sv_#'
DEBUG = True 
ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',  # Your custom app for user management
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'doctor_patient_management.urls'

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

WSGI_APPLICATION = 'doctor_patient_management.wsgi.application'

# Remove MySQL Database Configuration completely
DATABASES = {'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Using SQLite
        'NAME': BASE_DIR / 'db.sqlite3',         # Path to the SQLite file
    }}

# Firebase Firestore Configuration
db = firestore.client()

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# For Firebase authentication:
AUTH_USER_MODEL = 'users.CustomUser'   # Define your custom user model as needed
