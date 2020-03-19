from django.contrib import admin

from blog.models import *

# Register your models here.

class CategoryManager(admin.ModelAdmin):
    pass





class TagManager(admin.ModelAdmin):
    pass


class PostManager(admin.ModelAdmin):
    list_display = ['title','create_time','modified_time','category','author']
    fields = ['title','body','excerpt','category','tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request,obj,form,change)

    # pass


admin.site.register(Category,CategoryManager),
admin.site.register(Tag,TagManager),
admin.site.register(Post,PostManager),