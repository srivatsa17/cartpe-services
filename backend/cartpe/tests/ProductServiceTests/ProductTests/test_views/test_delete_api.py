from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product

# Initialize the APIClient app
client = APIClient()

class DeleteProductByIdTest(APITestCase):
    """ Test module for DELETE request for ProductByIdAPIView API """

    def get_url(self, productId):
        url = reverse('product_by_id', kwargs={'id': productId})
        return url

    def setUp(self) -> None:
        self.pixel = Product.objects.create(name = "pixel 7", description = "good product", price = 50000, stock_count = 10)

    def test_with_existing_id(self) -> None:
        expectedStatusCode = status.HTTP_204_NO_CONTENT

        url = self.get_url(self.pixel.id)
        response = client.delete(url)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_id(self) -> None:
        expectedResponse = "Unable to find product with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        response = client.delete(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)