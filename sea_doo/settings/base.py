from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog',
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

ROOT_URLCONF = 'sea_doo.urls'

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
                'catalog.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'sea_doo.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ro'
TIME_ZONE = 'Europe/Bucharest'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Site identity (override via .env or SiteSetting admin) ---
SITE_NAME = 'SeaDoo.ro'
SITE_TAGLINE = 'Prima comunitate serioasă de jet-ski din România'
SITE_DESCRIPTION = (
    'Colecție privată Sea-Doo, catalog tehnic complet, comunitate autentică '
    'și evenimente pe apă. Totul despre jet-ski în România.'
)
CONTACT_EMAIL = 'contact@seadoo.ro'
CONTACT_PHONE = ''
INSTAGRAM_URL = ''
TIKTOK_URL = ''
YOUTUBE_URL = ''

# --- Launch banner (toggle via SiteSetting in admin) ---
LAUNCH_BANNER_ENABLED = 'false'
LAUNCH_BANNER_TEXT = 'Comunitatea se lansează în curând — înscrie-te acum pe lista de așteptare!'
LAUNCH_BANNER_CTA_TEXT = 'Vreau să fiu primul'
LAUNCH_BANNER_CTA_URL = '/comunitate/#inscrie-te'

# --- Auth ---
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/profile/'
LOGOUT_REDIRECT_URL = '/'
