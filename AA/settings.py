from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-woktkro!x_%c^8$vkd03!(h*@6&7fd&e+2mq!gbv0%#ehvn@b6'
DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'ckeditor',
    'attachments',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'signuplogin.apps.SignuploginConfig',
    'clients',
    'settingsapp',
    'home',
    'jobs',
    'careersportal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'signuplogin.middleware.TenantMiddleware',  
    'allauth.account.middleware.AccountMiddleware',  
]
DATABASE_ROUTERS = ['AA.routers.TenantDatabaseRouter']

ROOT_URLCONF = 'AA.urls'
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
            ],
        },
    },
]

WSGI_APPLICATION = 'AA.wsgi.application'

import json
import os
# Load tenant databases configuration
databases_config_path = os.path.join(BASE_DIR, 'tenant_databases.json')
if os.path.exists(databases_config_path):
    with open(databases_config_path, 'r') as f:
        tenant_databases = json.load(f)
else:
    tenant_databases = {}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    **tenant_databases,
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'signuplogin.User'
AUTHENTICATION_BACKENDS = [
    'signuplogin.backends.AllowInactiveUserModelBackend',
]
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ankit@linksoft.net.in'
EMAIL_HOST_PASSWORD = 'Qwerty@12345678'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Koldboot <ankit@linksoft.net.in>'

# Microsoft OAuth
MS_AUTHORITY = "https://login.microsoftonline.com/common"  # Endpoint for authorization server
MS_CLIENT_ID = "36ddb5e2-646b-46be-bd4e-7df20dd5af82"  # Your Application (client) ID
MS_CLIENT_SECRET = "qEW8Q~SZrii-q1My-j-Y81NDWlbCx4ExnHyUNc_A"  # Your client secret
MS_REDIRECT_URI = "http://localhost:8000/settings/auth-callback2/"  # Your redirect URI
MS_SCOPES = ["User.Read", "Mail.Send", "Mail.Read", "offline_access", 'Calendars.ReadWrite']


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {  # This will handle logging for all of your project
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


CKEDITOR_UPLOAD_PATH = "ckeditor/uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono-lisa',  # the default skin
        'fontSize_sizes': '8/8px;9/9px;10/10px;11/11px;12/12px;14/14px;16/16px;18/18px;20/20px;22/22px;24/24px;26/26px;28/28px;30/30px;32/32px;34/34px;36/36px',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Full': [
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'SpecialChar', 'Iframe'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']
        ],
        'toolbar': 'Full',  # set the toolbar to use the "Full" toolbar we defined above
        'height': 300,
        'width': '100%',
        'filebrowserWindowWidth': 800,
        'filebrowserWindowHeight': 500,
        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserBrowseUrl': '/ckeditor/browse/',
        'removePlugins': 'elementspath',
        'resize_enabled': True,
        'extraPlugins': 'autogrow,divarea',
        'autoGrow_minHeight': 200,
        'autoGrow_maxHeight': 800,
        'autoGrow_bottomSpace': 10,
        'forcePasteAsPlainText': True,  # force pasted text to be plain
        'contentsCss': ['/static/css/ckeditor.css']  # custom styles for the editor content
    },
}


