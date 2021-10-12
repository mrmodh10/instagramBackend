import re

from django.views.decorators.csrf import requires_csrf_token
from rest_framework.exceptions import NotFound
from app.UserFolder.UserSerializer import UserSerializer
from rest_framework import viewsets
from django.http import response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from app.models import MyPost,User,Comment
from app.post.serializers import PostSerializer , PostSerializerForGet,CommentSerializerForGet,CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets, generics, status


class MyPostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = MyPost.objects.all()
    @api_view(['GET'])
    def getAllPost(self):
        queryset = MyPost.objects.all()
        s = PostSerializerForGet(queryset,many = True)
        data = {
            "status":1,
            "message":"sucess",
            "data":s.data
        }
        return response.JsonResponse(data)
    
    @api_view(['POST'])
    def createPost(request):
        user = Token.objects.get(key=str(request.data["token"])).user
        s = PostSerializer(data = request.data)
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
            return response.JsonResponse(data)
    
class LikeView(APIView):
    @api_view(['POST'])
    def get(request):
        try:
            post = MyPost.objects.get(pk=str(request.data["post_id"]))
            user = Token.objects.get(key=str(request.data["token"])).user
            if user in post.likes.all():
                like = False
                post.likes.remove(user)
            else:
                like = True
                post.likes.add(user)
            data = {
                "status" : 1,
                "message":"success",
                'like': like
            }
            return Response(data)
        except :
            data = {
                "status" : 0,
                "message":"In Valid Auth Key",
            }
            return Response(data)
    
class UserFeedView(generics.ListAPIView):
    @api_view(['POST'])
    def get_queryset(request):
        print(str(request.data["token"]))
        try:
            user = Token.objects.get(key=str(request.data["token"])).user
            userData = UserSerializer(user)
            following_users = user.following.all()
            queryset = MyPost.objects.all().filter(author__in=following_users)
            s = PostSerializerForGet(queryset,many = True)
            data = {
                "status" : 1,
                "message":"success",
                'data': {
                    "post":s.data
                }
            }
            return response.JsonResponse(data)
        except:
            data = {
            "status" : 0,
            "message":"fail",
            'data': []
            }
            return response.JsonResponse(data)
        

class ManageComment(viewsets.ModelViewSet):
    @api_view(['GET'])
    def getAllComment(self):
        queryset = Comment.objects.all()
        s = CommentSerializerForGet(queryset,many = True)
        data = {
            "status":1,
            "message":"sucess",
            "data":s.data
        }
        return response.JsonResponse(data)
    
    @api_view(['POST'])
    def getComment(request):
        queryset = Comment.objects.get(post=str(request.data["post_id"]))
        s = CommentSerializerForGet(queryset,many = True)
        data = {
            "status":1,
            "message":"sucess",
            "data":s.data
        }
        return response.JsonResponse(data)
    
    @api_view(['POST'])
    def AddComment(request):
        s = CommentSerializer(data = request.data)
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
            return response.JsonResponse(data)
    
    
    
    
            
            