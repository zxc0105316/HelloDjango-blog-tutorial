from django.shortcuts import render, redirect, HttpResponse
from blog.models import *
from django.shortcuts import get_object_or_404
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


# Create your views here.


def index(request):
    title = "首页"
    post_list = Post.objects.all()
    context = {"title": title, "post_list": post_list}
    return render(request, 'blog/index.html', context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                       'markdown.extensions.codehilite',
                                       'markdown.extensions.toc',
                                       # 这个用来做标题的锚点
                                       TocExtension(slugify=slugify)])

    post.body = md.convert(post.body)
    # re.S表示 . 现在也匹配换行符   re.M 表示^匹配每行的开头  $匹配每行的结尾
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''

    return render(request, 'blog/detail.html', context={'post': post})

# 归档
def archive(request,year,month):
    post_list = Post.objects.filter(create_time__year=year,
                                    create_time__month=month)

    context={'post_list':post_list}
    return render(request,'blog/index.html',context)


# 分类页面函数
def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate)
    context = {'post_list':post_list}
    return render(request,'blog/index.html',context)


# 标签页面函数
def tag(request,pk):
    tag = get_object_or_404(Tag,pk=pk)
    post_list = Post.objects.filter(tags=tag)
    context = {'post_list':post_list}
    return render(request,'blog/index.html',context)