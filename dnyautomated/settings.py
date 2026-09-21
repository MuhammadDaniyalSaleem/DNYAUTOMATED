from pathlib import Path
import os
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
SECRET_KEY=os.getenv('SECRET_KEY','dev-only-change-me')
DEBUG=os.getenv('DEBUG','True').lower()=='true'
ALLOWED_HOSTS=[h.strip() for h in os.getenv('ALLOWED_HOSTS','127.0.0.1,localhost').split(',') if h.strip()]
CSRF_TRUSTED_ORIGINS=[u.strip() for u in os.getenv('CSRF_TRUSTED_ORIGINS','').split(',') if u.strip()]
SECURE_SSL_REDIRECT=os.getenv('SECURE_SSL_REDIRECT','False').lower()=='true'
SESSION_COOKIE_SECURE=os.getenv('SESSION_COOKIE_SECURE','False').lower()=='true'
CSRF_COOKIE_SECURE=os.getenv('CSRF_COOKIE_SECURE','False').lower()=='true'
SECURE_HSTS_SECONDS=int(os.getenv('SECURE_HSTS_SECONDS','0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS=SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD=SECURE_HSTS_SECONDS > 0
X_FRAME_OPTIONS='DENY'
SECURE_CONTENT_TYPE_NOSNIFF=True
INSTALLED_APPS=['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','agency']
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF='dnyautomated.urls'
TEMPLATES=[{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[BASE_DIR/'agency'/'templates'],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION='dnyautomated.wsgi.application'
DATABASES={'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS=[]
LANGUAGE_CODE='en-us'; TIME_ZONE='Asia/Karachi'; USE_I18N=True; USE_TZ=True
STATIC_URL='static/'; STATICFILES_DIRS=[BASE_DIR/'agency'/'static']; STATIC_ROOT=BASE_DIR/'staticfiles'
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}
MEDIA_URL='media/'; MEDIA_ROOT=BASE_DIR/'media'
DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
LOGIN_URL='/client/login/'; LOGIN_REDIRECT_URL='/client/portal/'; LOGOUT_REDIRECT_URL='/'

# Email notifications (configure these in .env; never commit real passwords)
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'DNYAUTOMATED <noreply@localhost>')
LEAD_NOTIFICATION_EMAIL = os.getenv('LEAD_NOTIFICATION_EMAIL', EMAIL_HOST_USER)
EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', '15'))

AI_PROVIDER=os.getenv('AI_PROVIDER','gemini').lower()
AI_API_KEY=os.getenv('AI_API_KEY','')
AI_MODEL=os.getenv('AI_MODEL','gemini-2.0-flash')
AI_TIMEOUT=int(os.getenv('AI_TIMEOUT','25'))
CHATBOT_MAX_MESSAGE_LENGTH=int(os.getenv('CHATBOT_MAX_MESSAGE_LENGTH','1200'))
