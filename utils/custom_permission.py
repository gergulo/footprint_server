import re
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from common.models import User
from utils import security_util


#  获取用户权限
def get_user_permissions(user_id):
    # 从缓存获取用户权限
    permissions = security_util.get_user_permissions(user_id)
    if permissions is None:  # 无缓存
        try:
            # 从数据库读取用户权限
            user = User.objects.prefetch_related("roles").get(id=user_id)
            permissions = set()
            super_flag = False
            for role in user.roles.all():
                for permission in role.permissions.all():
                    # 超级管理员，退出循环
                    if permission.permission_value == "*":
                        permissions = set()
                        permissions.add(permission.permission_value)
                        super_flag = True
                        break
                    if permission.permission_type == 3:     # 只获取接口类型的权限配置
                        permissions.add(permission.permission_value)
                if super_flag:
                    break
            permissions = list(permissions)
            # 缓存用户权限
            security_util.cache_user_permissions(user_id, permissions)
        except ObjectDoesNotExist:  # 用户信息不存在
            permissions = None
    return permissions


class CustomPermission(BasePermission):
    """
    自定义权限判断类
    """

    message = {"code": 403, "msg": "用户未被授权访问，请联系管理员。"}

    # 重写 has_permission 方法，自定义权限判断规则
    def has_permission(self, request, view):
        user_id = request.user
        # 无用户信息或用户信息为匿名用户
        if user_id and not isinstance(user_id, AnonymousUser):
            # 从缓存里获取用户权限
            permissions = get_user_permissions(user_id)
            if permissions is not None:
                if "*" in permissions:  # 超级管理员
                    return True
                request_path = ("a" + request.path).replace("/", ":")    # 构建请求路径
                # print("请求接口权限：" + request_path)
                for permission in permissions:  # 匹配权限配置
                    result = re.match(permission, request_path)
                    # print("权限配置项：" + permission)
                    # print(result)
                    if result:
                        return True
        raise PermissionDenied(self.message)
