#__author: tzw 
# date: 2020/3/18

from django import template

from blog.models import Post,Category,Tag

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
    return {
        'category_list':Category.objects.all()
    }


#标签云模板标签
@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list':Tag.objects.all()
    }