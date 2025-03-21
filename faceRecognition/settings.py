"""
Django settings for faceRecognition project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)37&)id8=9xic6)l2)zo1$o_#px2un^d%d3%lb-b8uw533^vy9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    # 'drf_yasg', #
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'faceDet.apps.FacedetConfig',  # app
    'faceRec.apps.FacerecConfig',
    'serviceMgt.apps.ServicemgtConfig',
    'faceMgt.apps.FacemgtConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'faceRecognition.middleWares.responseMiddleware.ResponseMiddleware',  # 数据返回标准化封装
    # 'faceRecognition.middleWares.accessKeyCheckMiddleware.AccessKeyCheckMiddleware',  # 判定AK是否存在，且是否订购了此项能力
    # 'faceRecognition.middleWares.signValidationMiddleware.SignValidationMiddleware',  # 用户请求数据校验，判定数据是否被篡改
    # 请求体以及返回结果数据加解密
]

ROOT_URLCONF = 'faceRecognition.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'faceRecognition.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'faceServer.sqlite3',
    }
}
# DATABASES = {
#     'default':{
#         'ENGINE':'django.db.backends.mysql',
#         'NAME':'',
#         'HOST':'...',
#         'PORT':'',
#         'USER':'',
#         'PASSWORD':'',
#     }
# }

FEATURE_DB_DIR = os.path.join(BASE_DIR, "featureDB")
FEATURE_DB_REAL_TIME_UPDATE = True
FEATURE_DB_INIT_FILE = False
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# body 传输数据大小
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5M

#  日志
LOGGING_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGGING_DIR, exist_ok=True)
LOGGING_NAME = "faceRec"
LOGGING = {
    'version': 1,  # 使用的python内置的logging模块，那么python可能会对它进行升级，所以需要写一个版本号，目前就是1版本
    'disable_existing_loggers': False,  # 是否去掉目前项目中其他地方中以及使用的日志功能，但是将来我们可能会引入第三方的模块，里面可能内置了日志功能，所以尽量不要关闭。
    'formatters': {  # 日志记录格式
        'verbose': {  # levelname等级，asctime记录时间，module表示日志发生的文件名称，lineno行号，message错误信息
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 过滤器：可以对日志进行输出时的过滤用的
        'require_debug_true': {  # 在debug=True下产生的一些日志信息，要不要记录日志，需要的话就在handlers中加上这个过滤器，不需要就不加
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {  # 和上面相反
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {  # 日志处理方式，日志实例
        'console': {  # 在控制台输出时的实例
            'level': 'INFO',  # 日志等级；debug是最低等级，那么只要比它高等级的信息都会被记录
            'filters': ['require_debug_true'],  # 在debug=True下才会打印在控制台
            'class': 'logging.StreamHandler',  # 使用的python的logging模块中的StreamHandler来进行输出
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',  # DEBUG INFO
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建
            'filename': os.path.join(LOGGING_DIR, f"{LOGGING_NAME}.log"),  # 注意，你的文件应该有读写权限。os.path.dirname(
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
    },
    # 日志对象
    'loggers': {
        'django': {  # 和django结合起来使用，将django中之前的日志输出内容的时候，按照我们的日志配置进行输出，
            'handlers': ['console', 'file'],  # 将来项目上线，把console去掉
            'propagate': True,
            # 冒泡：是否将日志信息记录冒泡给其他的日志处理系统，工作中都是True，不然django这个日志系统捕获到日志信息之后，其他模块中可能也有日志记录功能的模块，就获取不到这个日志信息了
        },
    }
}

# 开放能力调用接口标识
OPEN_ABILITY_API_IDENTIFICATION = "ai/openAbility"

#
MEDIA_URL = '/mediaData/'
MEDIA_DIR = "mediaData"
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_DIR)

# DATETIME_FORMAT
DATETIME_FORMAT = "Y-m-d H:i:s"

# session setting
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60 * 5
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# body 传输数据大小
# DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5M
