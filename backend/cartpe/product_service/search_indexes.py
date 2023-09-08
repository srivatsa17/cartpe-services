from haystack import indexes
from product_service.models import Category

class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document = True, use_template = True)

    def get_model(self):
        return Category

    def index_queryset(self, using = None):
        """ Used when the entire index for model is updated. """
        return self.get_model().objects.all()