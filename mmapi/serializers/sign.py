from rest_framework import serializers
from common.models import Sign


class QuerySerialzer(serializers.ModelSerializer):
    """
    查询序列化器的参数定义
    """

    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=None)

    class Meta:
        model = Sign
        fields = [
            "id",
            "address",
            "lat",
            "lng",
            "create_time"
        ]
