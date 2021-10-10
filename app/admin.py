from django.contrib import admin
from .models import MyPost,User

admin.site.register(User)
admin.site.register(MyPost)


#@admin.register(MyPost)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ["text","number_of_likes"]