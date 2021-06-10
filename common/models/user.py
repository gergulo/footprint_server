from django.db import models


# 用户的模型
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, default="", verbose_name="姓名/微信昵称")
    openid = models.CharField(max_length=50, default="", verbose_name="微信openid")
    phone = models.CharField(max_length=20, default="", verbose_name="联系电话")
    remark = models.CharField(max_length=200, default="", verbose_name="备注说明")
    is_disable = models.IntegerField(default=0, verbose_name="状态：0.启用 1.停用")
    last_login_time = models.DateTimeField(null=True, blank=True, verbose_name="最后登录时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    class Meta:
        db_table = "tb_user"


# 用户微信信息的模型
class WXInfo(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=50, default="", verbose_name="微信openid")
    unionid = models.CharField(max_length=50, default="", verbose_name="微信unionId")
    nick_name = models.CharField(max_length=50, default="", verbose_name="微信昵称")
    avatar_url = models.CharField(max_length=250, default="", verbose_name="头像地址")
    gender = models.IntegerField(default=0, verbose_name="性别：0.未知 1.男 2.女")
    country = models.CharField(max_length=50, default="", verbose_name="国家")
    province = models.CharField(max_length=50, default="", verbose_name="省份")
    city = models.CharField(max_length=50, default="", verbose_name="城市")
    language = models.CharField(max_length=50, default="", verbose_name="语言")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="所属用户",
        related_name="wx_info_user"
    )

    class Meta:
        db_table = "tb_wx_info"