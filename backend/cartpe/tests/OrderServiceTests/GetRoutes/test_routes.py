from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

# Initialize the APIClient app
client = APIClient()


class GetRoutesTest(APITestCase):
    """Test module for GET request for RoutesAPIView API"""

    def get_url(self):
        url = reverse("order_routes")
        return url

    def test_get_routes(self):
        url = self.get_url()
        response = client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
