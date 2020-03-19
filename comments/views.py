from django.shortcuts import render,redirect,HttpResponse
from blog.models import *
from comments.forms import CommentForm
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from django.contrib import messages

# Create your views here.


@require_POST
def comment(request,post_pk):
    # 获取被评论的文章
    # get_object_or_404 方法执行成功返回 查询到的实体  失败返回一个404错误页面
    post = get_object_or_404(Post,pk=post_pk)


    # 将用户提交的表单的信息生成一个绑定用户提交数据的表单
    form = CommentForm(request.POST)

    # 当调用form.is_vaild()方法时，django自动检查表单的数据是否符合格式要求
    if form.is_valid():
        # 检查到数据是合法的，调用表单的save方法保存数据到数据库
        # commit=False  表示生成表单实例但是不保存到数据库
        comment = form.save(commit=False)

        # 将评论和被评论的文章关联
        comment.post = post

        # 最终将数据保存到数据库中。调用save方法

        comment.save()


        # 导入django的messages对象 add_message方法增加一条消息,这条是评论成功的时候发送的消息
        messages.add_message(request,messages.SUCCESS,'评论发表成功',extra_tags='success')

        print("success")
        # 重定向到post的详情页，实际上到redirect函数接收一个模型的实例时，它会调用这个模型实例的get_absolute_url
        # 然后重定向到get_absolute_url方法返回的URL.
        return redirect(post)

    # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
    # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
    context = {
        'post':post,
        'form':form,
    }
    # 定义一条评论失败发送的消息
    messages.add_message(request,messages.ERROR,'评论发表失败！请修改表单中的错误后重新提交。',extra_tags='danger')
    return render(request,'comments/preview.html',context=context)
