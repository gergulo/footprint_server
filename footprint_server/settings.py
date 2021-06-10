"""
Django settings for footprint_server project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from datetime import datetime, timedelta
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '69u$*qa6#*^*v$8crck1(fwixenxw1pxw$(*&dbuq_j9zzz-%_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',                  # 跨域支持
    'rest_framework',
    'rest_framework_swagger',
    'common',
    'mmapi',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',#放到中间件顶部
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'footprint_server.urls'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

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

WSGI_APPLICATION = 'footprint_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'footprint',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/5",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
        }
    }
}

REST_FRAMEWORK = {
    # 默认接口结构定义类
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.AutoSchema",
    # 默认认证类
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "utils.CustomAuthentication",
    ],
    # 默认权限判断类
    # "DEFAULT_PERMISSION_CLASSES": [
    #     "rest_framework.permissions.AllowAny",
    # ],
    "DEFAULT_PERMISSION_CLASSES": [
      "utils.CustomPermission",
    ],
    # 默认分页类，如果配置了，所有接口默认都会分页的参数
    # "DEFAULT_PAGINATION_CLASS": "utils.CustomPagination",
    # 默认每页记录条数
    'PAGE_SIZE': 10,
}

# swagger 配置项
SWAGGER_SETTINGS = {
    # 安全定义配置Swagger可以使用哪些身份验证方法。目前由OpenAPI的2.0规范支持的方案类型basic，apiKey和oauth2。
    "SECURITY_DEFINITIONS": {
        "basic": {
            "type": "basic"
        }
    },
    # 切换使用Django Auth作为身份验证机制。将其设置为True将会在Swagger UI上显示一个登录/注销按钮，并将csrf_tokens发布到API。
    # 默认： True
    "USE_SESSION_AUTH": False,
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的。
    # "LOGIN_URL": "rest_framework:login",      # 用于登录会话身份验证的URL。接受命名的URL模式。
    # "LOGOUT_URL": "rest_framework:logout",    # 用于注销会话身份验证的URL。接受命名的URL模式。
    # 接口文档中方法列表以首字母升序排列，默认： None。
    "APIS_SORTER": None,
    # 控制API列表的显示方式。可以设置为：None：所有操作均已折叠； "list"：列出所有操作；"full"：扩展所有操作。
    "DOC_EXPANSION": None,
    # 对每个API的操作列表进行排序。可以设置为："alpha"：按字母顺序排序；"method"：按HTTP方法排序。
    "OPERATIONS_SORTER": "alpha",
    # 如果支持json提交, 则接口文档中包含json输入框。
    "JSON_EDITOR": True,
    # 设置为True显示请求标头。
    "SHOW_REQUEST_HEADERS": True,
    # 可以使用“ Try it out! ”与HTTP方法列表进行交互。按钮。
    "SUPPORTED_SUBMIT_METHODS": ["get", "post", "put", "delete", "patch"],
    # swagger.io的在线模式验证器的URL。可以修改为指向本地安装，或设置None为禁用。
    "VALIDATOR_URL": None,
}

# 跨域相关
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-token'
)

# 默认Token有效时长
TOKEN_TIMEOUT = 7 * 24 * 60 * 60
# 默认密码
DEFAULT_PASSWORD = "12345678"

# 默认权限缓存时长
PERMISSIONS_CACHE_TIMEOUT = 5 * 60
# 默认用户组织信息缓存时长
ORGANIZATION_CACHE_TIMEOUT = 5 * 60

# 小程序配置
MINIPROGRAM_APPID = ""
MINIPROGRAM_APPSECRET = ""
# 跳转小程序类型：developer为开发版；trial为体验版；formal为正式版；默认为正式版
MINIPROGRAM_STATE = "developer"
WX_API_JS_CODE = "https://api.weixin.qq.com/sns/jscode2session?grant_type=authorization_code&js_code={0}&appid={1}&secret={2}"
WX_API_ACCESS_TOKEN = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"
WX_API_MSG_SEC_CHECK = "https://api.weixin.qq.com/wxa/msg_sec_check?access_token={0}"
WX_API_SUBSCRIBE_MSG_SEND = "https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={0}"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

FILE_URL = 'file/'
FILE_ROOT = os.path.join(BASE_DIR, 'file')

# 日志配置
# 创建日志的路径
LOG_PATH = os.path.join(BASE_DIR, 'log')
# 如果地址不存在，则自动创建log文件夹
if not os.path.join(LOG_PATH):
    os.mkdir(LOG_PATH)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] '
                      '[%(levelname)s]- %(message)s'},
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'collect': {
            'format': '[%(levelname)s][%(asctime)s] %(message)s'
        }
    },
    # 过滤
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'all-{}.log'.format(datetime.now().strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'error-{}.log'.format(datetime.now().strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 输出info日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'info-{}.log'.format(datetime.now().strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 输出info日志（收集信息使用）
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_PATH, 'collect-{}.log'.format(datetime.now().strftime('%Y-%m-%d'))),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': 'utf-8',  # 设置默认编码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {
            'handlers': ['default', 'console', 'error'],
            'level': 'INFO',
            'propagate': True
        },
        'log': {
            'handlers': ['info'],
            'level': 'INFO',
            'propagate': True
        },
        # collect 调用时需要当作参数传入
        'collect': {
            'handlers': ['collect'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}