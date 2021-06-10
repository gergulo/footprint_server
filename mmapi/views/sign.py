from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import EmptyPage
from django.http import JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from common.models import Sign
from mmapi.serializers import sign
from utils.schema_view import DocParam
from utils import CustomSerialzer, CustomPagination, file_util, constants, common_util


class UploadPhoto(GenericAPIView):
    """
    上传照片
    """

    # 接口参数定义
    core_api_fields = (
        DocParam("x-token", "header", True, "用户登录Token", "string"),
        DocParam("file", "formData", True, "文件", "file"),
    )
    # 默认序列化类
    serializer_class = CustomSerialzer
    # 权限判断类，不需要权限的接口，配置为[]，或[AllowAny, ]
    permission_classes = [AllowAny, ]

    # 方法定义
    def post(self, request):
        form = file_util.UploadFileForm(request.POST, request.FILES)  # 注意获取数据的方式
        if form.is_valid():
            (file_path, file_src_name, file_path2) = file_util.save_file(constants.sign_photo_path
                                                                         , request.FILES['file']
                                                                         , thumbnail=True, thumbnail_width=400)
            data = {
                "photo_url": file_path,
                "thumbnail_url": file_path2
            }
            result = {"code": 1, "msg": "照片上传成功", "data": data}
        else:
            result = {"code": 0, "msg": "照片无效"}
        return JsonResponse(result)


class DoSign(GenericAPIView):
    """
    打卡
    """

    # 接口参数定义
    core_api_fields = (
        DocParam("x-token", "header", True, "用户登录Token", "string"),
        DocParam("lng", "formData", True, "经度", "number"),
        DocParam("lat", "formData", True, "纬度", "number"),
        DocParam("address", "formData", True, "地址", "string"),
        DocParam("nation", "formData", True, "国家", "string"),
        DocParam("province", "formData", True, "省份", "string"),
        DocParam("city", "formData", True, "城市", "string"),
        DocParam("district", "formData", True, "区县", "string"),
        DocParam("street", "formData", True, "街道", "string"),
        DocParam("street_number", "formData", True, "门牌", "string"),
        DocParam("remark", "formData", True, "备注说明", "string"),
        DocParam("photo_url", "formData", True, "照片地址", "string"),
        DocParam("thumbnail_url", "formData", True, "照片缩略图地址", "string")
    )
    # 默认序列化类
    serializer_class = CustomSerialzer
    # 权限判断类，不需要权限的接口，配置为[]，或[AllowAny, ]
    permission_classes = [AllowAny, ]

    # 方法定义
    def post(self, request):
        lng = float(request.POST.get("lng", "0"))
        lat = float(request.POST.get("lat", "0"))
        address = request.POST.get("address", "")
        nation = request.POST.get("nation", "")
        province = request.POST.get("province", "")
        city = request.POST.get("city", "")
        district = request.POST.get("district", "")
        street = request.POST.get("street", "")
        street_number = request.POST.get("street_number", "")
        remark = request.POST.get("remark", "")
        photo_url = request.POST.get("photo_url", "")
        thumbnail_url = request.POST.get("thumbnail_url", "")

        try:
            sign_entity = Sign()
            sign_entity.lng = lng
            sign_entity.lat = lat
            sign_entity.address = address
            sign_entity.nation = nation
            sign_entity.province = province
            sign_entity.city = city
            sign_entity.district = district
            sign_entity.street = street
            sign_entity.street_number = street_number
            sign_entity.district = district
            sign_entity.remark = remark
            sign_entity.photo_url = photo_url
            sign_entity.thumbnail_url = thumbnail_url
            sign_entity.user_id = request.user
            sign_entity.save()
            result = {"code": 1, "msg": "打卡成功"}
        except:
            result = {"code": 0, "msg": "打卡失败"}
        return JsonResponse(result)


class GetList(GenericAPIView):
    """
    获取打卡列表
    """
    # 默认查询记录集
    queryset = Sign.objects.all().order_by("-id")
    # 默认序列化类
    serializer_class = CustomSerialzer
    # 权限判断类，不需要权限的接口，配置为[]，或[AllowAny, ]
    permission_classes = [AllowAny, ]
    # 分页类
    pagination_class = CustomPagination
    # 接口参数定义
    core_api_fields = (
        DocParam("current", "formData", True, "当前页码", "integer"),
        DocParam("size", "formData", True, "每页记录条数", "integer"),
        DocParam("query_date", "formData", False, "查询日期", "String"),
        DocParam("query_type", "formData", False, "查询类型", "integer"),
    )

    # 方法定义
    def post(self, request):
        # 查询
        query_date = request.POST.get("query_date", "")
        query_type = int(request.POST.get("query_type", "0"))
        queryset = self.get_queryset().filter(user_id=request.user)
        if query_date:
            begin_date = datetime.strptime(query_date, "%Y-%m-%d")
            if query_type == 0:     # 月份查询
                end_date = common_util.get_first_day_of_next_month(begin_date)
            else:   # 日期查询
                end_date = common_util.get_day(begin_date) + timedelta(days=1)
            queryset = queryset.filter(create_time__gte=begin_date, create_time__lt=end_date)
        try:
            # 分页查询
            page = self.paginate_queryset(queryset)
            # 数据序列化
            sr = sign.QuerySerialzer(instance=page, many=True)
            paging_info = self.paginator.get_paging_info()
            page = {
                "size": paging_info["page_size"],
                "current": paging_info["current_page"],
                "total": paging_info["total_count"],
                "pages": paging_info["total_pages"],
                "records": sr.data,
            }
            data = {
                "page": page
            }
            result = {"code": 1, "msg": "查询成功", "data": data}
        except EmptyPage:  # 空页，查询页码大于现有页码
            result = {"code": 0, "msg": "查询失败，已经是最后一页了"}
        return JsonResponse(result)


class GetDetail(GenericAPIView):
    """
    获取打卡信息
    """
    # 默认序列化类
    serializer_class = CustomSerialzer
    # 权限判断类，不需要权限的接口，配置为[]，或[AllowAny, ]
    permission_classes = [AllowAny, ]
    # 接口参数定义
    core_api_fields = (
        DocParam("x-token", "header", True, "用户登录Token", "string"),
        DocParam("id", "query", False, "id", "integer"),
    )

    # 方法定义
    def get(self, request):
        id = int(request.GET.get("id", "-1"))
        sign_entity = Sign.objects.select_related("user").filter(id=id).first()
        if sign_entity:
            data = {
                "id": sign_entity.id,
                "lng": sign_entity.lng,
                "lat": sign_entity.lat,
                "address": sign_entity.address,
                "photo_url": sign_entity.photo_url,
                "thumbnail_url": sign_entity.thumbnail_url,
                "remark": sign_entity.remark,
                "openid": sign_entity.user.openid,
                "create_time": sign_entity.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
            result = {"code": 1, "msg": "查询成功", "data": data}
        else:
            result = {"code": 0, "msg": "打卡信息不存在"}
        return JsonResponse(result)


class Delete(GenericAPIView):
    """
    删除打卡信息
    """

    # 接口参数定义
    core_api_fields = (
        DocParam("x-token", "header", True, "用户登录Token", "string"),
        DocParam("id", "query", True, "id", "integer"),
    )
    # 默认序列化类
    serializer_class = CustomSerialzer
    # 权限判断类，不需要权限的接口，配置为[]，或[AllowAny, ]
    permission_classes = [AllowAny, ]

    # 方法定义
    def get(self, request):
        id = int(request.GET.get("id", "0"))
        try:
            Sign.objects.get(id=id).delete()
            result = {"code": 1, "msg": "打卡信息删除成功"}
        except ObjectDoesNotExist:
            result = {"code": 0, "msg": "打卡信息不存在"}
        return JsonResponse(result)


class GetCount(GenericAPIView):
    """
    获取打卡数
    """

    # 接口参数定义
    core_api_fields = (
        DocParam("x-token", "header", True, "用户登录Token", "string"),
        DocParam("query_date", "formData", False, "查询日期", "String"),
    )
    # 默认序列化类
    serializer_class = CustomSerialzer
    # 权限判断类，不需要权限的接口，配置为[]，或[AllowAny, ]
    permission_classes = [AllowAny, ]

    # 方法定义
    def post(self, request):
        # 查询
        query_date = request.POST.get("query_date", "")
        print(query_date)
        queryset = Sign.objects.filter(user_id=request.user)
        if query_date:
            begin_date = datetime.strptime(query_date, "%Y-%m-%d")
            end_date = common_util.get_day(begin_date) + timedelta(days=1)
            queryset = queryset.filter(create_time__gte=begin_date, create_time__lt=end_date)
        data_count = queryset.count()
        data = {
            "data_count": data_count
        }
        result = {"code": 1, "msg": "查询成功", "data": data}
        return JsonResponse(result)
