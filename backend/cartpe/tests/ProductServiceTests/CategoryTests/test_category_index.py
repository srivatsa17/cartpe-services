from unittest.mock import Mock
from rest_framework.test import APITestCase, APIClient
from product_service.models import Category
from product_service.search_indexes import CategoryIndex

# Initialize the APIClient app
client = APIClient()


class CategoryIndexTestCase(APITestCase):
    """Test module for CategoryIndex class"""

    def test_get_model(self):
        category_index = CategoryIndex()

        self.assertEqual(category_index.get_model(), Category)

    def test_search(self):
        category_index = CategoryIndex()
        category_index.get_model = Mock(return_value=Mock(objects=Mock(all=Mock(return_value=[]))))
        queryset = category_index.index_queryset()

        self.assertEqual(queryset, [])
