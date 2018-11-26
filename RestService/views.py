from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegisterModuleSerializer, MessageModuleSerializer, PinModuleSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from .models import Register, PinModule, ErrorModule, SuccessModule
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import serializers
from django.db import transaction, IntegrityError


# Create your views here.


@api_view(['GET'])
def retrievemodule(request, format=None):
    try:
        for reg in Register.objects.all():
            for pin in PinModule.objects.all().filter(reg_module_id=reg.module_id):
                print(pin.pin_name)

        serializer =  RegisterModuleSerializer(reg)
    except ValueError as e:
        serializer = MessageModuleSerializer(ErrorModule(errorCode=e.args[0].pop("errorCode", None),
                                                       message=e.args[0].pop("message", None)))
    except Exception as e:
        print(e)
        serializer = MessageModuleSerializer(ErrorModule(errorCode="0000",
                                                       message="Please validate the data"))
        # CReate a log
    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

@api_view(['GET'])
def search(request, format=None):
    try:
        moduleSerial = request.query_params.get('serial', None)
        moduleAction = request.query_params.get('action', None)
        if moduleAction == 'CONF':
            # Need to call the MQTT to retrieve the specification.
            pinModuleList = []
            moduleDetails = {"serial": moduleSerial, "moduleName": "ABC"}
            for i in range(1, 4):
                pinModuleList.append(
                    {"pinName": "PinName" + str(i), "pinNo": i, "moduleType": "switch", "value": "1#0"})
            moduleDetails.update({'pinList': pinModuleList})
        else:
            raise ValueError({"errorCode": '1002', "message": 'Data error'})
    except ValueError as e:
        serializer = MessageModuleSerializer(ErrorModule(errorCode=e.args[0].pop("errorCode", None),
                                                       message=e.args[0].pop("message", None)))
    except Exception as e:
        serializer = MessageModuleSerializer(ErrorModule(errorCode="0000",
                                                       message=e))
    return JsonResponse(data=moduleDetails, status=status.HTTP_200_OK)


@api_view(['POST'])
def testmodule(request, format=None):
    try:
        data = JSONParser().parse(request)
        serializer = RegisterModuleSerializer(data=data)
        if serializer.is_valid():
            moduleSerial = serializer.validated_data.get('serial')
            pinList = serializer.validated_data.get('pinList')
            if pinList == None:
                raise ValueError({"errorCode": '1003', "message": 'Pin details not found in request'})
            pinList[0].update({'status': 'A'})
            pinModuleList = []
            for i in range(1, 3):
                pinModuleList.append(
                    PinModule(pinName="PinName" + str(i), pinNo=i, action="switch", value="1#0"))
            pinModuleList.append(PinModule(pinName=pinList[0].get('pinName'),
                                           pinNo=pinList[0].get('pinNo'),
                                           action=pinList[0].get('action'),
                                           value=pinList[0].get('value'),
                                           status=pinList[0].get('status'),
                                           ))
            serializer = RegisterModuleSerializer(Register(moduleSerial, pinModuleList), many=False)

    except ValueError as e:
        serializer = MessageModuleSerializer(ErrorModule(errorCode=e.args[0].pop("errorCode", None),
                                                       message=e.args[0].pop("message", None)))
    except Exception as e:
        serializer = MessageModuleSerializer(ErrorModule(errorCode="0000",
                                                       message="Please validate the data"))
        # CReate a log
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def saveModuleInfo(request, format=None):
    serializer = None
    try:
        with transaction.atomic():
            data = JSONParser().parse(request)
            register = Register()
            register.jsontoclass(data)
            register.save()
            for pinData in data['pinList']:
                pin = PinModule()
                pin.jsontoclass(pinData)
                pin.reg_module_id = register
                pin.save()
                serializer = MessageModuleSerializer(SuccessModule(successCode='0000',
                                                               message='Data get saved'))
    except ValueError as e:
        serializer = MessageModuleSerializer(ErrorModule(errorCode=e.args[0].pop("errorCode", None),
                                                       message=e.args[0].pop("message", None)))
    except IntegrityError as e:
        serializer = MessageModuleSerializer(ErrorModule(errorCode='0001',
                                                       message="Unable to save information"))
    except Exception as e:
        serializer = MessageModuleSerializer(ErrorModule(errorCode="0000",
                                                       message="Please validate the data"))
        print(e)
        # CReate a log
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)
