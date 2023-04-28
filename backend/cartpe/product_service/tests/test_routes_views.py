from rest_framework.test import APITestCase
from rest_framework import status
from django.test import Client
from django.urls import reverse

# Initialize the APIClient app
client = Client()

class GetRoutesTest(APITestCase):
    """ Test module for GET all supported routes API """

    def test_get_routes(self) -> None:
        response = client.get(reverse('routes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)