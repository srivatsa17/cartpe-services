from django.urls import reverse
from unittest.mock import patch, Mock
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Category
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()


class GetAllCategoriesTest(APITestCase):
    """Test module for GET request for CategoryAPIView API"""

    def get_url(self):
        url = reverse("categories")
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.men = Category.objects.create(name="Men", description="Clothing", parent=None)
        self.topwear = Category.objects.create(
            name="Topwear", description="Topwear for men", parent=self.men
        )

    def test_get_all_categories(self):
        url = self.get_url()
        response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class GetCategoryByIdTest(APITestCase):
    """Test module for GET request for CategoryByIdAPIView API"""

    def get_url(self, category_id):
        url = reverse("category_by_id", kwargs={"id": category_id})
        return url

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

        self.men = Category.objects.create(name="Men", description="Clothing", parent=None)
        self.topwear = Category.objects.create(
            name="Topwear", description="Topwear for men", parent=self.men
        )

    def test_get_category_by_id_with_valid_id(self):
        url = self.get_url(self.men.id)
        response = client.get(url)

        self.assertIsNotNone(response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_category_by_id_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.get(url)

        self.assertEqual("Unable to find category with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class SearchCategoriesTest(APITestCase):
    """Test module for GET request for CategorySearchAPIView API"""

    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="abcdef")
        client.force_authenticate(user=self.user)

    def get_url(self, searchKey=None):
        url = reverse("category_search") + f"?q={searchKey}"
        return url

    @patch("product_service.views.SearchQuerySet")
    def test_search_with_no_query_param(self, mock_search):
        mock_search_instance = mock_search.return_value
        mock_search_instance.filter.return_value = [
            Mock(id="product_service.category.1", text="['Men']", slug="['men']"),
            Mock(id="product_service.category.2", text="['Women']", slug="['women']"),
        ]

        url = self.get_url()
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            [{"id": 1, "name": "Men", "slug": "men"}, {"id": 2, "name": "Women", "slug": "women"}],
            response.data,
        )

    @patch("product_service.views.SearchQuerySet")
    def test_search_with_query_param(self, mock_search):
        mock_search_instance = mock_search.return_value
        mock_search_instance.filter.return_value = [
            Mock(id="product_service.category.1", text="['Men']", slug="['men']"),
            Mock(id="product_service.category.2", text="['Women']", slug="['women']"),
        ]

        url = self.get_url("me")
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            [{"id": 1, "name": "Men", "slug": "men"}, {"id": 2, "name": "Women", "slug": "women"}],
            response.data,
        )

    @patch("product_service.views.SearchQuerySet")
    def test_search_with_empty_response(self, mock_search):
        mock_search_instance = mock_search.return_value
        mock_search_instance.filter.return_value = []

        url = self.get_url("me")
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data)
