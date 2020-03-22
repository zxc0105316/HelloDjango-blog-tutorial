from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from blog.models import *
from django.shortcuts import get_object_or_404
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView
# 正常的类视图  重写get post方法
from django.views.generic import View
from pure_pagination import *
from django.contrib import messages


# Create your views here.

# def index(request):
#     title = "首页"
#     post_list = Post.objects.all()
#     context = {"title": title, "post_list": post_list}
#     return render(request, 'blog/index.html', context)

# 类视图的写法和上面的写法效果一致
# 这里还需要修改urls 为 as_view()
class IndexView(PaginationMixin, ListView):
    # 因为这里ListView父类中已经写好了分页逻辑。这里只需要调用
    # model。将 model 指定为 Post，告诉 django 我要获取的模型是 Post。
    # template_name。指定这个视图渲染的模板。
    # context_object_name。指定获取的模型列表数据保存的变量名，这个变量会被传递给模板。
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 设置每十篇文章一页
    paginate_by = 10


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     # 每次触发这个函数就给views加1
#     post.increase_views()
#
#     md = markdown.Markdown(extensions=['markdown.extensions.extra',
#                                        'markdown.extensions.codehilite',
#                                        'markdown.extensions.toc',
#                                        # 这个用来做标题的锚点
#                                        TocExtension(slugify=slugify)])
#
#     post.body = md.convert(post.body)
#     # re.S表示 . 现在也匹配换行符   re.M 表示^匹配每行的开头  $匹配每行的结尾
#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''
#
#     return render(request, 'blog/detail.html', context={'post': post})

# detail类视图
class PostDetailView(DetailView):
    # 这些属性的含义和ListView是一样
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 重写get方法
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 阅读量加1
        self.object.increase_views()

        # 视图必须返回一个HttpResponse对象
        return response

    # def get_object(self, queryset=None):
    #     # get_object本方法是获取post类的对象，但是这里需要对返回的post对象body做渲染
    #     # 重写get_object 对post的body进行渲染
    #     post = super().get_object(queryset=None)
    #     md = markdown.Markdown(extensions=['markdown.extensions.extra',
    #                                        'markdown.extensions.codehilite',
    #                                        'markdown.extensions.toc',
    #                                        # 这个用来做标题的锚点
    #                                        TocExtension(slugify=slugify)])
    #
    #     post.body = md.convert(post.body)
    #     # re.S表示 . 现在也匹配换行符   re.M 表示^匹配每行的开头  $匹配每行的结尾
    #     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    #     print(m.group(1))
    #     if m is not None:
    #         toc = m.group(1)
    #         print(toc)
    #     else:
    #         post.toc = ''
    #
    #      # if m is not None else ''
    #
    #
    #     # 返回渲染过post对象
    #     return post


# 归档
# def archive(request,year,month):
#     post_list = Post.objects.filter(create_time__year=year,
#                                     create_time__month=month)
#
#     context={'post_list':post_list}
#     return render(request,'blog/index.html',context)

# archive类视图
class ArchiveView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return super(ArchiveView, self).get_queryset().filter(create_time__year=self.kwargs.get('year'),
                                                              create_time__month=self.kwargs.get('month'))


# 分类页面函数
# def category(request,pk):
#     cate = get_object_or_404(Category,pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     context = {'post_list':post_list}
#     return render(request,'blog/index.html',context)

# 类视图重写
class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    # 重写方法
    # 这个方法默认获取的是当前声明的model的数据，也就是post的数据
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# 标签页面函数
# def tag(request,pk):
#     tag = get_object_or_404(Tag,pk=pk)
#     post_list = Post.objects.filter(tags=tag)
#     context = {'post_list':post_list}
#     return render(request,'blog/index.html',context)

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = '请输入搜索关键词'
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    # django.db.models    Q对象用于包装查询表达式
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {"post_list": post_list})
