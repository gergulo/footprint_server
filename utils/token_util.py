import json
import uuid
from django.conf import settings
from django.core.cache import cache

"""
登录Token的辅助类
"""


# 生成token，如有data，则写入Cache
def generate(data=None):
    token = str(uuid.uuid1()).replace('-', '').upper()
    if data is not None:
        write(token, data)
    return token, settings.TOKEN_TIMEOUT


# 从缓存中读取token内容
def read(token):
    key = 'token_' + token
    value = cache.get(key)
    if value is None:
        data = None
    else:
        data = value
    return data


# 将token内容写入缓存
def write(token, data):
    key = 'token_' + token
    cache.set(key, data, settings.TOKEN_TIMEOUT)


# 销毁token
def destroy(token):
    key = 'token_' + token
    cache.expire(key, 0)
