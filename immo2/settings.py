"""
Django settings for immo2 project.
Sécurisé pour la production — Acain Immobilier
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────
#  SECRET KEY — lue depuis variable d'environnement
# ─────────────────────────────────────────────────────────────
import secrets

def get_secret_key():
    key = os.environ.get('DJANGO_SECRET_KEY')
    if not key:
        import warnings
        warnings.warn(
            "\n⚠️  DJANGO_SECRET_KEY non définie ! Définissez-la en production.\n"
            "   export DJANGO_SECRET_KEY='votre-longue-cle-secrete'\n",
            stacklevel=2
        )
        key = secrets.token_urlsafe(50)  # temporaire, dev local uniquement
    return key

SECRET_KEY = get_secret_key()

# ─────────────────────────────────────────────────────────────
#  DEBUG — False en production
#  export DJANGO_DEBUG=False
# ─────────────────────────────────────────────────────────────
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# ─────────────────────────────────────────────────────────────
#  HÔTES AUTORISÉS
#  export DJANGO_ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
# ─────────────────────────────────────────────────────────────
_allowed = os.environ.get('DJANGO_ALLOWED_HOSTS', '')
ALLOWED_HOSTS = _allowed.split(',') if _allowed else ['127.0.0.1', 'localhost']

# ─────────────────────────────────────────────────────────────
#  APPLICATIONS
# ─────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'immo2app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'immo2app.middleware.LoginRequiredMessageMiddleware',
]

AUTH_USER_MODEL = 'immo2app.Utilisateur'
LOGIN_URL = 'connexion'

ROOT_URLCONF = 'immo2.urls'

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

WSGI_APPLICATION = 'immo2.wsgi.application'

# ─────────────────────────────────────────────────────────────
#  BASE DE DONNÉES
# ─────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─────────────────────────────────────────────────────────────
#  VALIDATION MOTS DE PASSE
# ─────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─────────────────────────────────────────────────────────────
#  INTERNATIONALISATION
# ─────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE     = 'Africa/Ndjamena'
USE_I18N = True
USE_L10N = True
USE_TZ   = True

# ─────────────────────────────────────────────────────────────
#  STATIQUES & MÉDIAS
# ─────────────────────────────────────────────────────────────
STATIC_URL      = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT     = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─────────────────────────────────────────────────────────────
#  LIMITES UPLOAD IMAGES
# ─────────────────────────────────────────────────────────────
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024   # 5 Mo max par requête
FILE_UPLOAD_MAX_MEMORY_SIZE  = 5 * 1024 * 1024  # 5 Mo max par fichier

ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
ALLOWED_IMAGE_TYPES      = ['image/jpeg', 'image/png', 'image/webp']
MAX_IMAGE_SIZE_MB        = 5

# ─────────────────────────────────────────────────────────────
#  SÉCURITÉ HTTPS (actif uniquement en production)
# ─────────────────────────────────────────────────────────────
if not DEBUG:
    SECURE_SSL_REDIRECT             = True
    SESSION_COOKIE_SECURE           = True
    CSRF_COOKIE_SECURE              = True
    SECURE_HSTS_SECONDS             = 31536000   # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
    SECURE_HSTS_PRELOAD             = True
    X_FRAME_OPTIONS                 = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF     = True
    SECURE_BROWSER_XSS_FILTER       = True

# Session expire à la fermeture du navigateur
SESSION_COOKIE_AGE          = 8 * 3600   # 8 heures max
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ─────────────────────────────────────────────────────────────
#  MESSAGES
# ─────────────────────────────────────────────────────────────
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.ERROR:   'error',
    message_constants.SUCCESS: 'success',
    message_constants.INFO:    'info',
    message_constants.WARNING: 'warning',
}
