from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import RegisterModuleSerializer, ErrorModuleSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from .models import Register, PinModule, ErrorModule
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser


# Create your views here.


@api_view(['GET'])
def search(request, format=None):
    try:
        moduleSerial = request.query_params.get('serial', None)
        moduleAction = request.query_params.get('action', None)
        if moduleAction == 'CONF':
            # Need to call the MQTT to retrieve the specification.
            pinModuleList = []
            for i in range(1, 4):
                pinModuleList.append(
                    PinModule(pinName="PinName" + str(i), pinNo=i, action="switch", value="1#0"))
            serializer = RegisterModuleSerializer(Register(moduleSerial, pinModuleList), many=False)

        else:
            raise ValueError({"errorCode": '1002', "message": 'Data error'})
    except ValueError as e:
        serializer = ErrorModuleSerializer(ErrorModule(errorCode=e.args[0].pop("errorCode", None),
                                                       message=e.args[0].pop("message", None)))
    except Exception as e:
        serializer = ErrorModuleSerializer(ErrorModule(errorCode="0000",
                                                       message=e))
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)


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
            pinList[0].update({'status':'A'})
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
        serializer = ErrorModuleSerializer(ErrorModule(errorCode=e.args[0].pop("errorCode", None),
                                                       message=e.args[0].pop("message", None)))
    except Exception as e:
        serializer = ErrorModuleSerializer(ErrorModule(errorCode="0000",
                                                       message="Please validate the data"))
        # CReate a log
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def saveModuleInfo(request, format=None):
    try:
        data = JSONParser().parse(request)
        serializer = RegisterModuleSerializer(data=data)
        if serializer.is_valid():
            moduleSerial = serializer.validated_data.get('serial')
            print(moduleSerial)
            serializer.save()

    except ValueError as e:
        serializer = ErrorModuleSerializer(ErrorModule(errorCode=e.args[0].pop("errorCode", None),
                                                       message=e.args[0].pop("message", None)))
    except Exception as e:
        serializer = ErrorModuleSerializer(ErrorModule(errorCode="0000",
                                                       message="Please validate the data"))
        # CReate a log
    return JsonResponse(serializer.data, status=status.HTTP_200_OK)




