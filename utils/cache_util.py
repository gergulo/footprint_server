from django.core.cache import cache

"""
缓存的辅助类
"""


# 从缓存中读取
def read(key):
    value = cache.get(key)
    if value is None:
        data = None
    else:
        data = value
    return data


# 将内容写入缓存
def write(key, data, timeout=None):
    cache.set(key, data, timeout)


# 销毁
def destroy(key):
    cache.expire(key, 0)
