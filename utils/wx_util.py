from django.conf import settings
import base64
from Crypto.Cipher import AES
import json
import logging
import requests
from utils import cache_util

_wx_token_key = "wx_token"
# 指定所用的logger
logger = logging.getLogger("collect")

"""
微信小程序相关
"""


def get_openid(code):
    """
    获取用户openid
    """
    url = settings.WX_API_JS_CODE.format(code, settings.MINIPROGRAM_APPID, settings.MINIPROGRAM_APPSECRET)
    result = requests.get(url)
    result = result.json()
    logger.info(result)
    return result


def decrypt_info(session_key, encrypted_data, iv):
    """
    解密获取用户信息，如个人信息、手机号码信息
    """
    pc = WXBizDataCrypt(settings.MINIPROGRAM_APPID, session_key)
    logger.info(encrypted_data)
    result = pc.decrypt(encrypted_data, iv)
    print(result)
    return result


def get_access_token():
    """
    获取微信access_token
    """
    wx_token = cache_util.read(_wx_token_key)
    if wx_token is None:
        url = settings.WX_API_ACCESS_TOKEN.format(settings.MINIPROGRAM_APPID, settings.MINIPROGRAM_APPSECRET)
        result = requests.get(url)
        result = result.json()
        logger.info(result)
        if result and "access_token" in result.keys():
            access_token = result["access_token"]
            expires_in = result["expires_in"] - 60
            cache_util.write(_wx_token_key, access_token, expires_in)
            result = {"code": 1, "msg": "请求成功", "data": access_token}
        else:
            if result and "errmsg" in result.keys():
                result = {"code": 0, "msg": result["errmsg"]}
            else:
                result = {"code": 0, "msg": "查询失败，请求微信接口失败"}
    else:
        result = {"code": 1, "msg": "查询成功", "data": wx_token}
    return result


def check_msg_sec(content):
    """
    敏感词检测
    """
    logger.info(content)
    token_result = get_access_token()
    logger.info(token_result)
    if token_result["code"] == 0:
        return token_result

    url = settings.WX_API_MSG_SEC_CHECK.format(token_result["data"])
    data = {
        "content": content.encode("utf-8").decode("latin1")
    }
    data = json.dumps(data, ensure_ascii=False)
    headers = {"content-type": "application/json;"}
    result = requests.post(url, data=data, headers=headers)
    result = result.json()
    logger.info(result)
    if result and result["errcode"] == 0:
        result = {"code": 1, "msg": "检测成功"}
    elif result and result["errcode"] == 40001:   # 如果提示access_token过去，则删除本地的access_token缓存
        cache_util.destroy(_wx_token_key)
        result = {"code": 0, "msg": "检测失败"}
    else:
        result = {"code": 0, "msg": "检测失败"}
    return result


def send_subscribe_msg(open_id, template_id, page, data):
    """
    发送订阅消息
    """
    token_result = get_access_token()
    logger.info(token_result)
    if token_result["code"] == 0:
        return token_result

    msg = {
        "touser": open_id,
        "template_id": template_id,
        "page": page,
        "miniprogram_state": settings.MINIPROGRAM_STATE,
        "data": data
    }
    logger.info(msg)
    url = settings.WX_API_SUBSCRIBE_MSG_SEND.format(token_result["data"])
    result = requests.post(url, json=msg)
    result = result.json()
    logger.info(result)
    if result and result["errcode"] == 40001:   # 如果提示access_token过去，则删除本地的access_token缓存
        cache_util.destroy(_wx_token_key)
    return result


class WXBizDataCrypt:
    """
    微信数据解密类
    """

    def __init__(self, app_id, session_key):
        self.app_id = app_id
        self.session_key = session_key

    def decrypt(self, encrypted_data, iv):
        # base64 decode
        b_session_key = base64.b64decode(self.session_key)
        b_encrypted_data = base64.b64decode(encrypted_data)
        b_iv = base64.b64decode(iv)

        cipher = AES.new(b_session_key, AES.MODE_CBC, b_iv)
        decrypted_data = self._unpad(cipher.decrypt(b_encrypted_data))
        try:
            decrypted = json.loads(decrypted_data)
        except UnicodeDecodeError:
            logger.info(encrypted_data)
            logger.info(iv)
            logger.info(self.session_key)
            decrypted = json.loads(decrypted_data, encoding='unicode_escape')
        if decrypted["watermark"]["appid"] != self.app_id:
            raise Exception("Invalid Buffer")
        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
