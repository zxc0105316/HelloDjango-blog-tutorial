from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

from django.urls import reverse
import markdown

# Create your models here.
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name="分类名")



    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100,verbose_name="标签名")

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Post(models.Model):



    # 文章标题

    title = models.CharField(max_length=70,verbose_name='标题')

    body = models.TextField(verbose_name='正文')

    create_time = models.DateTimeField(verbose_name="创建时间",default=timezone.now)
    modified_time = models.DateTimeField(verbose_name="修改时间")


    excerpt = models.CharField(max_length=200,blank=True,verbose_name="摘要")

    # 分类的外键关联，models.CASCADE表示级联删除
    category = models.ForeignKey('Category',on_delete=models.CASCADE,verbose_name="分类")
    # 标签的外键关联
    tags = models.ManyToManyField('Tag',blank=True,verbose_name="标签")


    # 新增views字段记录阅读量 editable 指不可后台修改
    views = models.PositiveIntegerField(default=0,editable=False)

    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="作者")
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']



    def __str__(self):
        return self.title

    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])


    # 重写了父类的save方法，同时要在方法内再调用父类的save方法
    def save(self,*args,**kwargs):
        self.modified_time = timezone.now()
        # 实例化markdown类用于渲染body的文本

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body)[:54])
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
