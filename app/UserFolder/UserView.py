from rest_framework import viewsets
from django.http import response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from app.models import User 
from app.UserFolder.UserSerializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from json import loads, dumps


class UserViewClass(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    @api_view(['POST'])
    def getAllUser(request):
        user = Token.objects.get(key=str(request.data["token"])).user
        queryset = User.objects.all()
        s = UserSerializer(queryset,many = True)
        for i in s.data:
            if(user.id in i['followers']):
                i.update({'followed_by_current_user':True})
            else:
                i.update({'followed_by_current_user':False})
        data = {
            "status":1,
            "message":"sucess",
            "data":s.data
        }
        return response.JsonResponse(data)
    
    @api_view(['POST'])
    def getUser(request):
        queryset = Token.objects.get(key=str(request.data["token"])).user
        s = UserSerializer(queryset)
        data = {
            "status":1,
            "message":"sucess",
            "data":s.data
        }
        return response.JsonResponse(data)
    
    @api_view(['POST'])
    def registrationAndLogin(request):
        user = User.objects.filter(email=request.data["email"]).first()
        # If user existd
        if user is not None:
            token, created = Token.objects.get_or_create(user_id=user.id)
            s = UserSerializer(user)
            print(token)
            return response.JsonResponse({
                'status': 1,
                'msg':"Success",
                'data':{
                'user':s.data,
                'token': token.key  
                }
            })
            
        # return Response({'User exist'})
        # If user don't exst
        serializer = UserSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            print('Ser', serializer.data)
            token = Token.objects.get(user_id=serializer.data['id'])
            return Response({
                'status': 1,
                'msg':"Success",
                'user':serializer.data,
                'token':token.key
            })
        
        return Response({'Invalid data for user'})
        
        
        
    
class FollowUserView(APIView):
    @api_view(['POST'])
    def addOrRemoveFollower(request):
        to_user = User.objects.get(id=str(request.data["other_user_id"]))
        from_user = Token.objects.get(key=str(request.data["token"])).user
        follow = None
        if from_user.is_authenticated:
            if from_user != to_user:
                if from_user in to_user.followers.all():
                    follow = False
                    from_user.following.remove(to_user)
                    to_user.followers.remove(from_user)
                else:
                    follow = True
                    from_user.following.add(to_user)
                    to_user.followers.add(from_user)
        data = {
            'follow': follow
        }
        return Response(data)