from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Category

# Initialize the APIClient app
client = APIClient()

class DeleteCategoryByIdTest(APITestCase):

    """ Test module for DELETE request for CategoryByIdAPIView API """

    def get_url(self, categoryId):
        url = reverse('category_by_id', kwargs={'id' : categoryId})
        return url

    def setUp(self) -> None:
        self.men = Category.objects.create(name = "Men", description = "Clothing", parent = None)

    def test_with_existing_id(self) -> None:
        expectedStatusCode = status.HTTP_204_NO_CONTENT

        url = self.get_url(self.men.id)
        response = client.delete(url)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_id(self) -> None:
        expectedResponse = "Unable to find category with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        response = client.delete(url)
        receivedResponse = str(response.data['message'])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)