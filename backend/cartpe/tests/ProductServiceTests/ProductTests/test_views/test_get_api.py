from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from product_service.models import Product
from product_service.serializers import ProductSerializer

# Initialize the APIClient app
client = Client()

class GetAllProductsTest(APITestCase):
    """ Test module for GET request for ProductAPIView API """

    def get_url(self):
        url = reverse('products')
        return url

    def setUp(self) -> None:
        Product.objects.create(name = "iphone 13", description = "ok product", price = 70000, stock_count = 1)
        Product.objects.create(name = "pixel 7", description = "good product", price = 50000, stock_count = 10)

    def test_valid_data(self) -> None:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many = True)
        expectedResponse = serializer.data
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url()
        response = client.get(url)
        receivedResponse = response.data
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

class GetProductByIdTest(APITestCase):
    """ Test module for GET request for ProductByIdAPIView API """

    def get_url(self, productId):
        url = reverse('product_by_id', kwargs = { 'id' : productId })
        return url

    def setUp(self) -> None:
        self.iphone = Product.objects.create(name = "iphone 13", description = "ok product", price = 70000, stock_count = 1)
        self.pixel = Product.objects.create(name = "pixel 7", description = "good product", price = 50000, stock_count = 10)

    def test_with_valid_id(self) -> None:
        product = Product.objects.get(id = self.pixel.pk)
        serializer = ProductSerializer(product, many = False)
        expectedResponse = serializer.data
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.pixel.id)
        response = client.get(url)

        receivedResponse = response.data
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_non_existing_id(self) -> None:
        expectedResponse = "Unable to find product with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        response = client.get(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)