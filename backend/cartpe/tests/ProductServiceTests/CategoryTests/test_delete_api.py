from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Category
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

class DeleteCategoryByIdTest(APITestCase):
    """ Test module for DELETE request for CategoryByIdAPIView API """

    def get_url(self, category_id):
        url = reverse("category_by_id", kwargs = { "id" : category_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.men = Category.objects.create(name = "Men", description = "Clothing", parent = None)

    def test_delete_with_existing_id(self):
        url = self.get_url(self.men.id)
        response = client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertIsNone(response.data)

    def test_delete_with_non_existing_id(self):
        url = self.get_url(1000)
        response = client.delete(url)

        self.assertEqual("Unable to find category with id 1000", str(response.data["message"]))
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
