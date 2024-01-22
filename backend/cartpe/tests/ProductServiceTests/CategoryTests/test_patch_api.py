from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from product_service.models import Category
from auth_service.models import User

# Global variables
CONTENT_TYPE = "application/json"

# Initialize the APIClient app
client = APIClient()

class UpdateCategoryByIdTest(APITestCase):
    """ Test module for PATCH request for CategoryByIdAPIView API """

    def get_url(self, category_id):
        url = reverse("category_by_id", kwargs = { "id" : category_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.men = Category.objects.create(name = "Men", description = "Clothing", parent = None)
        self.women = Category.objects.create(name = "Women", description = "Clothing for women", parent = None)
        self.topwear = Category.objects.create(name = "Topwear", description = "Topwear for men", parent = self.men)
        self.footwear = Category.objects.create(name = "Footwear", description = "Footwear for men", parent = self.men)

    def test_update_with_valid_input(self):
        url = self.get_url(self.men.id)
        data = json.dumps({
            "id": 20,
            "name": "abc",
            "description": "good one",
            "slug": "abcd"
        })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual(self.men.id, response.data["id"])
        self.assertEqual("abc", response.data["name"])
        self.assertEqual("good one", response.data["description"])
        self.assertEqual("abc", response.data["slug"])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_with_parent(self):
        url = self.get_url(self.men.id)
        data = json.dumps({ "parent" : "Clothes" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Object with name=Clothes does not exist.", response.data["parent"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_with_child(self):
        url = self.get_url(self.topwear.id)
        data = json.dumps({ "parent" : "Women" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Women", response.data["parent"])
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_field_with_empty_input(self):
        url = self.get_url(self.men.id)
        data = json.dumps({ "name" : "" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("This field may not be blank.", response.data["name"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_with_non_existing_id(self):
        url = self.get_url(1000)
        data = json.dumps({ "name" : "" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("Unable to find category with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_with_existing_name_and_parent(self):
        url = self.get_url(self.topwear.id)
        data = json.dumps({ "name" : "Footwear", "parent" : "Men" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("The fields name, parent must make a unique set.", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_update_with_same_name_and_no_parent(self):
        url = self.get_url(self.men.id)
        data = json.dumps({ "name" : "men", "parent" : None })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)

        self.assertEqual("The fields name, parent must make a unique set.", response.data["message"][0])
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
