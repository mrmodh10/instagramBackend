
from django.contrib import admin
from django.urls import path
from app.post.views import MyPostView, LikeView, UserFeedView,ManageComment
from app.NotificationFolder.NotificationView import NotificationView
from app.UserFolder.UserView import UserViewClass,FollowUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/',MyPostView.getAllPost),
    path('allUsers/',UserViewClass.getAllUser),
    path('user/',UserViewClass.getUser),
    path('like/',LikeView.get),
    path('addOrRemoveFollower/',FollowUserView.addOrRemoveFollower),
    path('userFeed/',UserFeedView.get_queryset),
    path('login/',UserViewClass.registrationAndLogin),
    path('createPost/',MyPostView.createPost),
    path('getAllcomment/',ManageComment.getAllComment),
    path('addcomment/',ManageComment.AddComment),
    path('getAllNotifiation/',NotificationView.getAllNotification),
    path('addNotifiation/',NotificationView.AddNotification)
]
