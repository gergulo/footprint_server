from django.urls import path

from .views import user, sign

urlpatterns = [
    # 小程序，用户相关
    path("mmapi/user/login", user.Login.as_view()),
    path("mmapi/user/update_info", user.UpdateInfo.as_view()),
    # 小程序，打卡相关
    path("mmapi/sign/upload_photo", sign.UploadPhoto.as_view()),
    path("mmapi/sign", sign.DoSign.as_view()),
    path("mmapi/sign/list", sign.GetList.as_view()),
    path("mmapi/sign/detail", sign.GetDetail.as_view()),
    path("mmapi/sign/delete", sign.Delete.as_view()),
    path("mmapi/sign/count", sign.GetCount.as_view())
]
