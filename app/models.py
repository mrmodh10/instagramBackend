from os import write
import re
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from instagram import settings
import uuid
import os


def image_file_path(instance, filename):
    """Generate file path for new recipe image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/', filename)


#user model
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=11)
    is_verified = models.BooleanField(default=False)
    last_login_time = models.IntegerField(null=True)
    last_logout_time = models.IntegerField(null=True)
    created_time = models.DateTimeField(auto_now_add=True, blank=True)
    fcm_token = models.TextField(null=True,blank=True)
    password = models.CharField(max_length=225,null=True)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    social_id = models.CharField(max_length=225,null=True)
    profile_pic = models.ImageField(upload_to="Item_Images",null = True, default = "")
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="user_followers",
                                       blank=True,
                                       symmetrical=False,)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="user_following",
                                       blank=True,
                                       symmetrical=False,)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def number_of_followers(self):
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

    def number_of_following(self):
        if self.following.count():
            return self.following.count()
        else:
            return 0
        
    def followers_list(self):
        followerslist = []
        for p in self.followers.all():
            data = {
                "name":p.first_name,
                "email":p.email
            } 
            followerslist.append(data)
        return followerslist
    
    def following_list(self):
        followinglist = []
        for p in self.following.all():
            data = {
                "name":p.first_name,
                "email":p.email
            } 
            followinglist.append(data)
        return followinglist
        
    def __str__(self):
        return self.email


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
        
class MyPost(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_posts',
        null=True
    )
    photo = models.ImageField(upload_to="Item_Images",null = True)
    text = models.TextField(max_length=500, blank=True,null=True)
    location = models.CharField(max_length=30, blank=True,null=True)
    posted_on = models.DateTimeField(auto_now_add=True,null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="likers",
                                   blank=True,
                                   symmetrical=False)
    

    class Meta:
        ordering = ['-posted_on']

    def number_of_likes(self):
        if self.likes.count():
            return self.likes.count()
        else:
            return 0
        
    def liked_by(self):
        userList = []
        for p in self.likes.all():
            data = {
                "name":p.first_name,
                "email":p.email
            } 
            userList.append(data)
        return userList
    
    def __str__(self):
        return f'{self.author}\'s post'
    

class Comment(models.Model):
    post = models.ForeignKey('MyPost',
                             on_delete=models.CASCADE,
                             related_name='post_comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='user_comments')
    text = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_on']

    def __str__(self):
        return f'{self.author}\'s comment'
    
class Notification(models.Model):
    title = models.TextField(null=True)
    dec = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='author')
    receiver =  models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='receiver')
    status = models.IntegerField()
    seen = models.BooleanField(default=False)
       
    class Meta:
        ordering = ['-date']


