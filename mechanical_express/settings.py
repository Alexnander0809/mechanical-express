import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-dlz_qkzy8!i)2!g!*!k#rhyu(ji$5ypkj-^u($eltg9z81dx5l'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']  # Ajusta según tus necesidades

INSTALLED_APPS = [
    'client',
    'mechanical_express',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Backend por defecto
    'client.backends.EmailBackend',  # Nuestro backend personalizado
]


SESSION_ENGINE = 'django.contrib.sessions.backends.db'


ROOT_URLCONF = 'client.urls'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'client', 'templates')],  # Asegúrate de que esto apunte a la carpeta templates en la raíz del proyecto
        'APP_DIRS': True,  # Esto debe estar en False ya que no estás usando apps
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


WSGI_APPLICATION = 'mechanical_express.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mechanical_express',
        'USER': 'root',
        'PASSWORD': '',  # Usa una variable de entorno para la contraseña
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

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




LANGUAGE_CODE = 'es-co'  # Cambiado a español

TIME_ZONE = 'America/Bogota'  # Cambiado a la zona horaria de Colombia

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'client', 'Public'),
]

AUTH_USER_MODEL = 'client.CustomerUser'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'client', 'Public', 'img', 'mecanicos')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'alexvalderramaguisao@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')  # Usa una variable de entorno para la contraseña

LOGIN_URL = 'login'  # Redirige aquí si no estás autenticado
LOGIN_REDIRECT_URL = ''  # Dónde redirigir tras iniciar sesión
LOGOUT_REDIRECT_URL = 'login'  # Dónde redirigir tras cerrar sesión
