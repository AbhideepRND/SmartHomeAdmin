from rest_framework import serializers
from .models import PinModule, Register, ErrorModule


class PinModuleSerializer(serializers.ModelSerializer):
    pinName = serializers.CharField(max_length=15, source="pin_name")
    pinNo = serializers.IntegerField(required=True, source="pin_no")
    type = serializers.CharField(max_length=10, source="module_type")
    value = serializers.CharField(max_length=10)
    status = serializers.CharField(max_length=1, required=False)

    class Meta:
        model = PinModule
        fields = '__all__'


class RegisterModuleSerializer(serializers.ModelSerializer):
    # SM-01ESP0000001 -
    serial = serializers.CharField(max_length=15)
    module_name = serializers.CharField(max_length=20)
    pinList = PinModuleSerializer(many=True)

    class Meta:
        model = Register
        fields = ('serial', 'module_name', 'pinList',)


class MessageModuleSerializer(serializers.Serializer):
    errorCode = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=20)

    def create(self, **modData):
        return ErrorModule(modData)
