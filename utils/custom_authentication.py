from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed
from utils import security_util


class CustomAuthentication(BasicAuthentication):
    """
    自定义认证类
    """
    # 重写 authenticate 方法，自定义认证规则
    def authenticate(self, request):
        # token验证
        result = security_util.verify_token(request)
        if result["code"] == 1:
            return result["user_data"]["id"], result["token"]
        else:
            raise AuthenticationFailed(result)


