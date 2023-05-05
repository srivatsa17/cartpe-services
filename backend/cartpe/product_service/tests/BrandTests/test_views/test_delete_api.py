from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from product_service.models import Brand

# Initialize the APIClient app
client = Client()

class DeleteBrandByIdTest(APITestCase):

    """ Test module for DELETE request for BrandByIdAPIView API """

    def get_url(self, brandId):
        url = reverse('brand_by_id', kwargs={'id': brandId})
        return url

    def setUp(self) -> None:
        self.google = Brand.objects.create(name = "google", description = "good brand")

    def test_with_existing_id(self) -> None:
        expectedResponse = "Brand 'google' deleted successfully."
        expectedStatusCode = status.HTTP_204_NO_CONTENT

        url = self.get_url(self.google.id)
        response = client.delete(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_id(self) -> None:
        expectedResponse = "Unable to find brand with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        response = client.delete(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)