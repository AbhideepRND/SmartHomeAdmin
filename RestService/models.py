from django.db import models


# Create your models here.

class Register(models.Model):
    module_id = models.AutoField(primary_key=True)
    serial = models.CharField(max_length=15)
    module_name = models.CharField(max_length=20)

    class Meta:
        db_table = u'RestService_register'

    def jsontoclass(self, data):
        self.serial = data.get('serial', None)
        self.module_name = data.get('moduleName', None)


class PinModule(models.Model):
    pin_id = models.AutoField(primary_key=True)
    pin_name = models.CharField(max_length=15)
    pin_no = models.IntegerField(null=False)
    module_type = models.CharField(max_length=10)
    value = models.CharField(max_length=10)
    status = models.CharField(max_length=1, null=True)
    reg_module_id = models.ForeignKey(Register, on_delete=models.CASCADE)

    class Meta:
        db_table = u'RestService_pinmodule'

    def jsontoclass(self, data):
        self.pin_name = data.get('pinName', None)
        self.pin_no = data.get('pinNo', None)
        self.module_type = data.get('moduleType', None)
        self.value = data.get('value', None)
        self.status = data.get('status', None)


class ErrorModule():
    def __init__(self, **kwargs):
        self.errorCode = kwargs.pop("errorCode", None)
        self.message = kwargs.pop("message", None)

class SuccessModule():
    def __init__(self, **kwargs):
        self.errorCode = kwargs.pop("successCode", None)
        self.message = kwargs.pop("message", None)