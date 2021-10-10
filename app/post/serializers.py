from os import read
from rest_framework import serializers
from app.models import MyPost,Comment
from django.contrib.auth import get_user_model


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for object author info"""

    class Meta:
        model = get_user_model()
        fields = ("first_name",'last_name','profile_pic')
        
class CommentSerializerForGet(serializers.ModelSerializer):
    """Serializer for the comment objects"""
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'posted_on')
        read_only_fields = ('author', 'id', 'posted_on')


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the post objects"""
    class Meta:
        model = MyPost
        fields =('id', 'author', 'photo',
                  'text', 'location', 'posted_on',
                  'number_of_likes','liked_by')
        
class PostSerializerForGet(serializers.ModelSerializer):
    """Serializer for the post objects"""
    author = AuthorSerializer(read_only=True)
    post_comments = CommentSerializerForGet(read_only=True,many = True)
    class Meta:
        model = MyPost
        fields =('id', 'author', 'photo',
                  'text', 'location', 'posted_on',
                  'number_of_likes','liked_by','post_comments')
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','post','author', 'text', 'posted_on')
        

        