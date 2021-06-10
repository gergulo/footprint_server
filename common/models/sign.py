from django.db import models
from .user import User


# 打卡的模型
class Sign(models.Model):
    id = models.AutoField(primary_key=True)
    lng = models.FloatField(default=0, verbose_name="经度")
    lat = models.FloatField(default=0, verbose_name="纬度")
    address = models.CharField(max_length=200, default="", verbose_name="地址")
    nation = models.CharField(max_length=50, default="", verbose_name="国家")
    province = models.CharField(max_length=50, default="", verbose_name="省份")
    city = models.CharField(max_length=50, default="", verbose_name="城市")
    district = models.CharField(max_length=50, default="", verbose_name="区县")
    street = models.CharField(max_length=50, default="", verbose_name="街道")
    street_number = models.CharField(max_length=50, default="", verbose_name="门牌")
    remark = models.CharField(max_length=200, default="", verbose_name="备注说明")
    photo_url = models.CharField(max_length=200, default="", verbose_name="照片地址")
    thumbnail_url = models.CharField(max_length=200, default="", verbose_name="照片缩略图地址")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="所属用户",
        related_name="sign_user"
    )

    class Meta:
        db_table = "tb_sign"
