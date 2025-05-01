from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pwxla-&uuzq#1qetkz2b-0&qyk_)!k%yt%=i(bragcsy0x9wy3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Em produção, esse valor deve ser False para maior segurança.

ALLOWED_HOSTS = []  # Permite que o Django reconheça domínios de onde pode receber requisições

# Definindo o modelo de usuário customizado.
AUTH_USER_MODEL = 'users.User'  # A referência ao modelo de usuário da app 'users'

# Application definition

INSTALLED_APPS = [
    # Apps padrão do Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Django REST Framework (DRF) para criação da API RESTful
    'rest_framework',
    
    # Middleware para permitir requisições de origens diferentes (CORS)
    'corsheaders',
    
    # App de usuários para a customização do modelo de usuário
    'users',
    
    # Djoser para gerenciamento de autenticação de usuários com JWT
    'djoser',
    
    # Para usar tokens com Django REST Framework
    'rest_framework.authtoken',
    
    # Para documentação da API (Swagger)
    'drf_yasg',
]

# Configuração do Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Autenticação via token
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Autenticação via JWT
    ],
}

# Configuração do JWT (JSON Web Token) para autenticação
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # O token de acesso expira após 15 minutos
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # O token de atualização expira após 7 dias
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Middleware para permitir CORS
    'corsheaders.middleware.CorsMiddleware',  
    
    # Middleware para lidar com requisições comuns
    'django.middleware.common.CommonMiddleware',
]

# Permite que o frontend (geralmente em localhost) tenha acesso ao backend no Django.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # O frontend React está rodando em localhost:5173
]

ROOT_URLCONF = 'cme_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Não estamos usando templates HTML do Django no backend, então a lista está vazia
        'APP_DIRS': True,  # Permite que o Django procure templates dentro dos diretórios de cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cme_project.wsgi.application'


# Database
# Configuração para o banco de dados PostgreSQL. O Django se conectará a um serviço de banco de dados chamado 'db' no Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Usando PostgreSQL como banco de dados
        'NAME': 'cme_db',  # Nome do banco de dados
        'USER': 'postgres',  # Usuário do banco de dados
        'PASSWORD': '123',  # Senha do banco de dados
        'HOST': 'db',  # O serviço de banco de dados é chamado 'db' no Docker Compose
        'PORT': '5432',  # A porta padrão do PostgreSQL
    }
}


# Password validation
# Configuração para validação de senhas. Pode ser personalizado conforme as regras de segurança da sua aplicação
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
# Configuração de internacionalização. O idioma padrão está em inglês (en-us) e o fuso horário é UTC.
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'  # Fuso horário UTC
USE_I18N = True  # Habilita internacionalização
USE_TZ = True  # Habilita uso de fusos horários

# Static files (CSS, JavaScript, Images)
# Configuração para arquivos estáticos. Como não estamos servindo arquivos estáticos diretamente no Django (backend),
STATIC_URL = 'static/'

# Default primary key field type
# Define o tipo padrão para a chave primária dos modelos.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
