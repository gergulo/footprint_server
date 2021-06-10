from rest_framework import serializers


class CustomSerialzer(serializers.Serializer):
    '''
    自定义对象序列化器
    '''
    class Meta:
        fields = "__all__"