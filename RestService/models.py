from django.db import models


# Create your models here.

class Register(models.Model):
    module_id = models.AutoField(primary_key=True)
    serial = models.CharField(max_length=15)

    def __init__(self, serial, pinList=[]):
        self.serial = serial
        self.pinList = pinList


class PinModule(models.Model):
    pin_id = models.AutoField(primary_key=True)
    pinName = models.CharField(max_length=15)
    pinNo = models.IntegerField(null=False)
    action = models.CharField(max_length=10)
    value = models.CharField(max_length=10)
    status = models.CharField(max_length=1,null=True)
    Reg_Module_id = models.ForeignKey(Register, on_delete=models.CASCADE)

    def __init__(self, **kwargs):
        self.pinName = kwargs.pop('pinName', None)
        self.pinNo = kwargs.pop('pinNo', None)
        self.action = kwargs.pop('action', None)
        self.value = kwargs.pop('value', None)
        self.status = kwargs.pop('status', 'I')


class ErrorModule():
    def __init__(self, **kwargs):
        self.errorCode = kwargs.pop("errorCode", None)
        self.message = kwargs.pop("message", None)
