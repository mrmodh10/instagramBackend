from rest_framework import serializers
from app.models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'date_joined',  'email','fcm_token',
                  'mobile', 'first_name', 'last_name',
                  'profile_pic','followers','followers_list',"following_list")