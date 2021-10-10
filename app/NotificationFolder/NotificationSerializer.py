from os import read
from rest_framework import serializers
from app.models import Notification
from app.UserFolder import UserSerializer



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        
class NotificationSerializerGet(serializers.ModelSerializer):
    author = UserSerializer.UserSerializer(read_only=True)
    receiver = UserSerializer.UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = "__all__"