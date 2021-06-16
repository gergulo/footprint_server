import hashlib
import random
import uuid
from django.conf import settings
from utils import cache_util

_salt_source = "abcdefghijklmnopqrstuvwxyz"   # 密码盐随机字符范围
_salt_length = 8                              # 密码盐长度
_token_key = "token_"
_permissions_key = "permissions_"
_organization_key = "organization_"

"""
安全的辅助类
"""


# 密码相关
# 生成新密码
def generate_new_password(src=""):
    if src == "":
        src = settings.DEFAULT_PASSWORD
    dict_salt = generate_salt()  # 生成密码盐信息
    result = generate_password(src, dict_salt[1])  # 生成密码
    return result, dict_salt[0]


# 生成密码盐信息
def generate_salt(src=""):
    if src == "":
        src = "".join(random.sample(_salt_source, _salt_length))
    hl = hashlib.md5()
    hl.update(src.encode(encoding="utf-8"))
    return src, hl.hexdigest().upper()


# 生成密码
def generate_password(password, salt_password):
    hl = hashlib.md5()
    hl.update(password.encode(encoding="utf-8"))
    password = hl.hexdigest().upper()
    hl = hashlib.md5()
    hl.update((password + salt_password).encode(encoding="utf-8"))
    password = hl.hexdigest().upper()
    return password


# 验证密码
def verify_password(input_password, db_password, salt):
    dict_salt = generate_salt(salt)  # 生成密码盐信息
    password = generate_password(input_password, dict_salt[1])  # 生成密码
    return password == db_password


# token相关
# 生成token
def generate_token(user_data, client_type=0):
    token = str(uuid.uuid1()).replace('-', '').upper()
    if client_type == 0:
        timeout = settings.TOKEN_TIMEOUT
    else:
        timeout = None
    if user_data is not None:
        cache_util.write(_token_key + token, user_data, timeout)
    return token, timeout


# 验证token
def verify_token(request):
    token = request.META.get("HTTP_X_TOKEN")
    if token is None:
        return {"code": 401, "msg": "无效登录信息，请重新登录。"}
    # 通过token获取用户信息
    user_data = cache_util.read(_token_key + token)
    if user_data is None:
        return {"code": 401, "msg": "用户已注销登录或登录过期，请重新登录。"}

    return {"code": 1, "msg": "验证成功", "user_data": user_data, "token": token}


# 销毁token
def destroy_token(request):
    token = request.META.get("HTTP_X_TOKEN")
    if token is None:
        return {"code": 401, "msg": "无效登录信息，请重新登录。"}

    cache_util.destroy(_token_key + token)


# 更新用户信息
def update_user_data(token, user_data):
    cache_util.write(_token_key + token, user_data)


# 获取用户信息
def get_user_data(request):
    token = request.META.get("HTTP_X_TOKEN")
    if token is None:
        return {"code": 401, "msg": "无效登录信息，请重新登录。"}

    return cache_util.read(_token_key + token)


# 用户信息相关
# 缓存用户权限
def cache_user_permissions(user_id, permissions):
    if permissions is not None:
        cache_util.write(_permissions_key + str(user_id), list(permissions), settings.PERMISSIONS_CACHE_TIMEOUT)


# 获取用户权限
def get_user_permissions(user_id):
    result = cache_util.read(_permissions_key + str(user_id))
    if result is None:
        return None
    else:
        return result


# 销毁用户权限
def destroy_user_permissions(user_id):
    cache_util.destroy(_permissions_key + str(user_id))
