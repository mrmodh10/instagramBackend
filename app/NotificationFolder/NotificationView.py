import re
from django.dispatch.dispatcher import receiver
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.exceptions import NotFound
from app.UserFolder.UserSerializer import UserSerializer
from rest_framework import viewsets
from django.http import response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from app.models import Notification,User
from app.NotificationFolder.NotificationSerializer import NotificationSerializer, NotificationSerializerGet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, generics, status
from pyfcm import FCMNotification


class NotificationView(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    @api_view(['POST'])
    def getAllNotification(request):
        user = Token.objects.get(key=str(request.data["token"])).user
        queryset = Notification.objects.filter(receiver=user)
        count = 0
        for i in queryset:
            if(i.seen==False):
                count = count + 1
        s = NotificationSerializerGet(queryset,many = True)
        data = {
            "status":1,
            "message":"sucess",
            "data":s.data,
            "count":count
        }
        return response.JsonResponse(data)
    
    @api_view(['POST'])
    def AddNotification(request):
        user = User.objects.filter(id = request.data['receiver']).first()
        print(user.fcm_token)
        push_service = FCMNotification(api_key="AAAAlK_2D7c:APA91bHmN9d1rHDVzSbD6qYQElrekXcovkLBT8CUQBH4pMfCdnn-MqwLPH153b7S4BkcdbkQDTa2BtZbxSeJK7PXxBGqY-sz0LMkK6zrVzDSJmjmDdYRGop1fj2Oq90WP48ITixebcKI")
        registration_id = user.fcm_token
        message_title = request.data['title']
        message_body = request.data['dec']
        data_message = {
            "Nick" : "Mario",
            "body" : "great match!",
            "Room" : "PortugalVSDenmark"
        }
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,  message_body=message_body, data_message=data_message,low_priority=False)
        print(result)
        data = {
            "result":result
        }
        s = NotificationSerializer(data = request.data)
        if s.is_valid():
            s.save()
            data = {
                "status":1,
                "message":"data saved successfully"
            }
            return response.JsonResponse(data)
        else:
            message = s.error_messages
            print(message)
            data = {
                "status":0,
                "message":"all fields are required"
            }
        return response.JsonResponse({"data":"h"})