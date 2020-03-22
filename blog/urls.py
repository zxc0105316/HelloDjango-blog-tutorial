"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import views
from blog.feeds import AllPostsRssFeed


app_name = "blog"
urlpatterns = [

    path('',views.IndexView.as_view(),name='index'),
    # <int:pk>   表示接收一个int数据 并把这个数据传给pk 提交到后台
    path('posts/<int:pk>/',views.PostDetailView.as_view(),name='detail'),
    path('archives/<int:year>/<int:month>',views.ArchiveView.as_view(),name='archive'),
    path('categories/<int:pk>/',views.CategoryView.as_view(),name='category'),
    path('tags/<int:pk>/',views.TagView.as_view(),name='tag'),

    #
    path('all/rss/',AllPostsRssFeed(),name='rss'),

    #
    # path('search/',views.search,name='search'),
]
