#__author: tzw 
# date: 2020/3/18

from django import template
from comments.forms import CommentForm

register = template.Library()

@register.inclusion_tag('comments/inclusions/_form.html',takes_context=True)
def show_comment_form(context,post,form=None):
    # post是文章对象 form是表单commentsform对象
    if form is None:
        form = CommentForm()
    return {
        'form':form,
        'post':post,
    }



@register.inclusion_tag('comments/inclusions/_list.html',takes_context=True)
def show_comments(context,post):
    comment_list = post.comment_set.all().order_by('-create_time')
    comment_count = comment_list.count()
    context = {'comment_count':comment_count,
               'comment_list':comment_list,
            }
    return context