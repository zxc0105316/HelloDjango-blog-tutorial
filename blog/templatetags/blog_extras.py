#__author: tzw 
# date: 2020/3/18

from django import template

from blog.models import Post,Category,Tag
from django.db.models.aggregates import Count

# 将方法包装为模板标签

register = template.Library()

#最新文章模板标签
@register.inclusion_tag("blog/inclusions/_receent_posts.html", takes_context=True)
def show_recent_posts(context,num=5):
    return {
        'recent_post_list':Post.objects.all()[:num]
    }


# 按月归档模板标签
@register.inclusion_tag("blog/inclusions/_archives.html", takes_context=True)
def show_archives(context):
    return {
        "date_list":Post.objects.dates('create_time','month',order="DESC")
    }


# 分类模板标签
@register.inclusion_tag("blog/inclusions/_categories.html", takes_context=True)
def show_categories(context):
    # 获取分类标签下关联的post文章数，只获取有大于0篇的文章的标签的post文章数
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list':category_list,
    }


#标签云模板标签
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list':tag_list
    }