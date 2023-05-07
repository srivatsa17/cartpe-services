from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json, decimal
from product_service.models import Product, Category, Brand

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = Client()

class UpdateProductByIdTest(APITestCase):
    """ Test module for PATCH request for ProductByIdAPIView API """

    def get_url(self, productId):
        url = reverse('product_by_id', kwargs={'id' : productId})
        return url

    def setUp(self) -> None:
        self.category = Category.objects.create(name = "Electronics")
        self.pixel = Product.objects.create(name="pixel 7", description="good product", price=50000, stock_count=10, discount=0)

    def test_product_id(self) -> None:
        expectedResponse = self.pixel.id
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "id" : 20 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['id']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_product_name(self) -> None:
        expectedResponse = "abc"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "name" : "abc" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['name']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_product_sku(self) -> None:
        expectedResponse = str(self.pixel.sku)
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "sku" : "a42c3fa7-a0be-45a9-ae06-61835f2cf64e" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['sku']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_description(self) -> None:
        expectedResponse = "good phone"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "description" : "good phone" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['description']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_slug(self) -> None:
        expectedResponse = self.pixel.slug
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "slug" : "abcd" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['slug']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_price(self) -> None:
        expectedResponse = decimal.Decimal('70000.90')
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "price" : 70000.90 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['price']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_brand(self) -> None:
        self.brand = Brand.objects.create(name = "apple")
        expectedResponse = "apple"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "brand" : "apple"})
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = str(response.data['brand'])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_stock_count(self) -> None:
        expectedResponse = 15
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "stock_count" : 15})
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['stock_count']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_discount(self) -> None:
        expectedResponse = 10
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "discount" : 10 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['discount']
        receivedStatusCode = response.status_code

        self.assertEqual(response.data['discounted_price'], decimal.Decimal('5000'))
        self.assertEqual(response.data['selling_price'], 45000)
        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_category(self) -> None:
        self.category = Category.objects.create(name = "Phone")
        expectedResponse = "Phone"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "category" : "Phone" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = str(response.data['category'])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_name_with_empty_input(self) -> None:
        expectedResponse = "This field may not be blank."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "name" : "" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['name'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_id(self) -> None:
        expectedResponse = "Unable to find product with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        data = json.dumps({ "name" : "" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_same_name(self) -> None:
        expectedResponse =  "Product 'pixel 7' already exists and cannot be created or updated again."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.pixel.id)
        data = json.dumps({ "name" : "pixel 7" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)