#__author: tzw 
# date: 2020/3/22

# 这个文件是django haystack搜索引擎的配置文件

# 注意建立数据模板的路径

# templates/search/indexes/youapp/\<model_name>_text.txt

from haystack import indexes
from .models import Post

# 这个类名是固定的 (model_name)Index
class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()