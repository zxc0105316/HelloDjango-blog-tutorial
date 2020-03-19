#__author: tzw 
# date: 2020/3/18


from django.urls import path

from comments import views

app_name = 'comments'

urlpatterns = [

    path('comment/<int:post_pk>',views.comment,name='comment'),

]