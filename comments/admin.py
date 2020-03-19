from django.contrib import admin

from  comments.models import *

# Register your models here.


class CommentManager(admin.ModelAdmin):
    list_display = ['name','email','url','post','create_time']
    fields = ['name','email','url','post','create_time']


admin.site.register(Comment,CommentManager)