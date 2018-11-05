from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import PinModule, Register, ErrorModule


class PinModuleSerializer(serializers.Serializer):
    pinName = serializers.CharField(max_length=15)
    pinNo = serializers.IntegerField(required=True)
    action = serializers.CharField(max_length=10)
    value = serializers.CharField(max_length=10)
    status = serializers.CharField(max_length=1, required=False)

    class Meta:
        model = PinModule
        fields = '__all__'


class RegisterModuleSerializer(serializers.Serializer):
    # SM-01ESP0000001 -
    serial = serializers.CharField(max_length=15)
    pinList = PinModuleSerializer(many=True)

    class Meta:
        model = Register
        fields = ('serial', 'pinList')


class ErrorModuleSerializer(serializers.Serializer):
    errorCode = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=20)

    def create(self, **modData):
        return ErrorModule(modData)
