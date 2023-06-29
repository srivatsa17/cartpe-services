from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from product_service.models import Category, Brand

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = APIClient()

class PostProductTest(APITestCase):
    """ Test module for POST request for ProductAPIView API """

    def get_url(self):
        url = reverse('products')
        return url

    def setUp(self) -> None:
        self.category = Category.objects.create(name = "Electronics")
        self.brand = Brand.objects.create(name = "Cannon")
        self.validData = {
            "name" : "DSLR",
            "description" : "Amazing",
            "brand" : "Cannon",
            "category" : "Electronics",
            "price" : 929.99,
            "stock_count" : 5,
            "discount" : 0
        }

    def test_with_valid_data(self) -> None:
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url()
        data = json.dumps(self.validData)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_name(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "description" : "Amazing", "brand" : "Cannon", "category" : "Electronics", "price" : 929.99, "stock_count" : 5, "discount" : 0 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['name'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_description(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "name" : "DSLR", "brand" : "Cannon", "category" : "Electronics", "price" : 929.99, "stock_count" : 5, "discount" : 0 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['description'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_price(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "name" : "DSLR", "description" : "Amazing", "brand" : "Cannon", "category" : "Electronics", "stock_count" : 5, "discount" : 0 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['price'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_brand(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "name" : "DSLR", "description" : "Amazing", "category" : "Electronics", "price" : 929.99, "stock_count" : 5, "discount" : 0 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['brand'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_stock_count(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "name" : "DSLR", "description" : "Amazing", "brand" : "Cannon", "category" : "Electronics", "price" : 929.99, "discount" : 0 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['stock_count'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_discount(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "name" : "DSLR", "description" : "Amazing", "brand" : "Cannon", "category" : "Electronics", "price" : 929.99, "stock_count" : 5 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['discount'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_category(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "name" : "DSLR", "description" : "Amazing", "brand" : "Cannon", "price" : 929.99, "stock_count" : 5, "discount" : 0 })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['category'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_post_product_with_same_name(self) -> None:
        expectedResponse = "Product 'DSLR' already exists and cannot be created or updated again."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps(self.validData)
        client.post(url, data = data, content_type = CONTENT_TYPE)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)