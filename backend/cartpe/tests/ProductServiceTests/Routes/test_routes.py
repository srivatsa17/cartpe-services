from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

# Initialize the APIClient app
client = Client()

class GetRoutesTest(APITestCase):
    """ Test module for GET request for RoutesAPIView API """

    def get_url(self):
        url = reverse('product-routes')
        return url

    def test_get_routes(self) -> None:
        expectedResponse = status.HTTP_200_OK

        url = self.get_url()
        response = client.get(url)
        receivedResponse = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)