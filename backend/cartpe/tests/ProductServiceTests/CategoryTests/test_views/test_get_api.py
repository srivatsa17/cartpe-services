from django.urls import reverse
from unittest.mock import patch, Mock
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Category
from product_service.serializers import CategorySerializer
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

class GetAllCategoriesTest(APITestCase):
    """ Test module for GET request for CategoryAPIView API """

    def get_url(self):
        url = reverse('categories')
        return url

    def setUp(self) -> None:
        self.men = Category.objects.create(name = "Men", description = "Clothing", parent = None)
        self.topwear = Category.objects.create(name = "Topwear", description = "Topwear for men", parent = self.men)

    def test_get_all_categories(self) -> None:
        categories = Category.objects.root_nodes()
        serializer = CategorySerializer(categories, many = True)
        expectedResponse = serializer.data
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url()
        response = client.get(url)
        receivedResponse = response.data
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

class GetCategoryByIdTest(APITestCase):
    """ Test module for GET request for CategoryByIdAPIView API """

    def get_url(self, categoryId):
        url = reverse('category_by_id', kwargs = { 'id' : categoryId })
        return url

    def setUp(self) -> None:
        self.men = Category.objects.create(name = "Men", description = "Clothing", parent = None)
        self.topwear = Category.objects.create(name = "Topwear", description = "Topwear for men", parent = self.men)

    def test_get_category_by_id_with_valid_id(self) -> None:
        category = Category.objects.get(id = self.men.pk)
        serializer = CategorySerializer(category, many = False)
        expectedResponse = serializer.data
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.men.id)
        response = client.get(url)
        receivedResponse = response.data
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_get_category_by_id_with_non_existing_id(self) -> None:
        expectedResponse = "Unable to find category with id 100"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(100)
        response = client.get(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

class SearchCategoriesTest(APITestCase):
    """ Test module for GET request for CategorySearchAPIView API """

    def setUp(self):
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

    def get_url(self, searchKey=None):
        url = reverse('category_search') + f"?q={searchKey}"
        return url

    @patch("product_service.views.SearchQuerySet")
    def test_search_with_no_query_param(self, mock_search):
        mock_search_instance = mock_search.return_value
        mock_search_instance.filter.return_value = [
            Mock(id='product_service.category.1', text="['Men']"),
            Mock(id='product_service.category.2', text="['Women']"),
        ]
        expectedStatusCode = status.HTTP_200_OK
        expectedResponse = [
            {"id": 1, "name": "Men"},
            {"id": 2, "name": "Women"}
        ]

        url = self.get_url()
        response = client.get(url)
        receivedStatusCode = response.status_code
        receivedResponse = response.data

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)

    @patch("product_service.views.SearchQuerySet")
    def test_search_with_query_param(self, mock_search):
        mock_search_instance = mock_search.return_value
        mock_search_instance.filter.return_value = [
            Mock(id='product_service.category.1', text="['Men']"),
            Mock(id='product_service.category.2', text="['Women']")
        ]
        expectedStatusCode = status.HTTP_200_OK
        expectedResponse = [
            {"id": 1, "name": "Men"},
            {"id": 2, "name": "Women"}
        ]

        url = self.get_url("me")
        response = client.get(url)
        receivedStatusCode = response.status_code
        receivedResponse = response.data

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)

    @patch("product_service.views.SearchQuerySet")
    def test_search_with_empty_response(self, mock_search):
        mock_search_instance = mock_search.return_value
        mock_search_instance.filter.return_value = []
        expectedStatusCode = status.HTTP_200_OK
        expectedResponse = []

        url = self.get_url("me")
        response = client.get(url)
        receivedStatusCode = response.status_code
        receivedResponse = response.data

        self.assertEqual(expectedStatusCode, receivedStatusCode)
        self.assertEqual(expectedResponse, receivedResponse)