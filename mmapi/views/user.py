from datetime import datetime
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from common.models import User, WXInfo
from utils.schema_view import DocParam
from utils import security_util, CustomSerialzer, wx_util


class Login(GenericAPIView):
    """
    提交code，进行登录/注册，返回用户信息
    """
    # 默认序列化类
    serializer_class = CustomSerialzer
    # 认证类，不需要登录的接口，配置为[]
    authentication_classes = []
    # 权限判断类，不需要权限的接口，配置为[]，或[AllowAny, ]
    permission_classes = [AllowAny, ]
    # 接口参数定义
    core_api_fields = (
        DocParam("code", "formData", True, "小程序登录返回code", "string"),
    )

    # 方法定义
    def post(self, request):
        code = request.POST.get("code", "")
        if code:
            result = wx_util.get_openid(code)
            if result and "openid" in result.keys():
                openid = result['openid']
                session_key = result['session_key']
                user_entity = User.objects\
                    .prefetch_related("wx_info_user") \
                    .filter(openid=openid)\
                    .first()
                wx_info_entity = None
                if not user_entity:   # 无用户，则注册
                    user_entity = User()
                    user_entity.openid = openid
                    user_entity.last_login_time = datetime.now()
                    user_entity.save()
                else:
                    User.objects.filter(id=user_entity.id).update(last_login_time=datetime.now())
                    wx_info_entity = user_entity.wx_info_user.first()
                user_data = {
                    "id": user_entity.id,
                    "type": 0,
                    "session_key": session_key
                }
                (token, expire) = security_util.generate_token(user_data)
                avatar_url = ""
                gender = 0
                has_wx_info = 0
                if wx_info_entity:
                    avatar_url = wx_info_entity.avatar_url
                    gender = wx_info_entity.gender
                    has_wx_info = 1
                data = {
                    "token": token,
                    "expired_time": expire,
                    "has_wx_info": has_wx_info,
                    "user_info": {
                        "openid": user_entity.openid,
                        "nickname": user_entity.name,
                        "phone": user_entity.phone,
                        "avatar": avatar_url,
                        "gender": gender
                    }
                }
                result = {"code": 1, "msg": "登录成功", "data": data}
            else:
                if result and "errmsg" in result.keys():
                    result = {"code": 0, "msg": result['errmsg']}
                else:
                    result = {"code": 0, "msg": "查询失败，请求微信接口失败"}
        else:
            result = {"code": 0, "msg": "查询失败，小程序登录返回code不能为空"}
        return JsonResponse(result)


class UpdateInfo(GenericAPIView):
    """
    更新用户信息
    """
    # 默认序列化类
    serializer_class = CustomSerialzer
    # 认证类，不需要登录的接口，配置为[]
    # 权限判断类，不需要权限的接口，配置为[]，或[AllowAny, ]
    permission_classes = [AllowAny, ]
    # 接口参数定义
    core_api_fields = (
        DocParam("encrypted_data", "formData", True, "包括敏感数据在内的完整用户信息的加密数据", "string"),
        DocParam("iv", "formData", True, "加密算法的初始向量", "string"),
    )

    # 方法定义
    def post(self, request):
        encrypted_data = request.POST.get("encrypted_data", "")
        iv = request.POST.get("iv", "")
        if encrypted_data and iv:
            result = security_util.verify_token(request)
            if result["code"] == 1:
                session_key = result["user_data"]["session_key"]
                user_id = result["user_data"]["id"]
                # try:
                # 解密得到用户信息
                wx_result = wx_util.decrypt_info(session_key, encrypted_data, iv)
                # except:
                #     result = {"code": 0, "msg": "解密微信用户信息失败"}
                # else:
                # 保存用户信息
                try:
                    user_entity = User.objects \
                        .prefetch_related("wx_info_user") \
                        .get(id=user_id)
                    wx_info_entity = user_entity.wx_info_user.first()
                    if not wx_info_entity:
                        wx_info_entity = WXInfo()
                        wx_info_entity.user_id = user_id
                    with transaction.atomic():
                        nick_name = wx_result['nickName']
                        openid = user_entity.openid
                        # 保存用户微信信息
                        wx_info_entity.openid = openid
                        wx_info_entity.nick_name = nick_name
                        wx_info_entity.country = wx_result['country']
                        wx_info_entity.province = wx_result['province']
                        wx_info_entity.city = wx_result['city']
                        wx_info_entity.avatar_url = wx_result['avatarUrl']
                        wx_info_entity.language = wx_result['language']
                        wx_info_entity.gender = wx_result['gender']
                        wx_info_entity.save()
                        # 保存用户信息
                        user_entity.name = nick_name
                        user_entity.save()
                    data = {
                        "openid": wx_info_entity.openid,
                        "nickname": wx_info_entity.nick_name,
                        "phone": user_entity.phone,
                        "avatar": wx_info_entity.avatar_url,
                        "gender": wx_info_entity.gender
                    }
                    result = {"code": 1, "msg": "更新用户信息成功", "data": data}
                except ObjectDoesNotExist:
                    result = {"code": 0, "msg": "更新用户信息失败，用户基础信息不存在"}
        else:
            result = {"code": 0, "msg": "更新用户信息失败，请求参数不能为空"}
        return JsonResponse(result)
