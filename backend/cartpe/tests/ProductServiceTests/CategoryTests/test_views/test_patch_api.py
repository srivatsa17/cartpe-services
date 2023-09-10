from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from product_service.models import Category
from auth_service.models import User

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = APIClient()

class UpdateCategoryByIdTest(APITestCase):
    """ Test module for PATCH request for CategoryByIdAPIView API """

    def get_url(self, categoryId):
        url = reverse('category_by_id', kwargs={'id' : categoryId})
        return url

    def setUp(self) -> None:
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.men = Category.objects.create(name = "Men", description = "Clothing", parent = None)
        self.women = Category.objects.create(name = "Women", description = "Clothing for women", parent = None)
        self.topwear = Category.objects.create(name = "Topwear", description = "Topwear for men", parent = self.men)
        self.footwear = Category.objects.create(name = "Footwear", description = "Footwear for men", parent = self.men)

    def test_with_id(self) -> None:
        expectedResponse = self.men.id
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.men.id)
        data = json.dumps({ "id" : 20 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['id']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_name(self) -> None:
        expectedResponse = "abc"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.men.id)
        data = json.dumps({ "name" : "abc" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['name']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_description(self) -> None:
        expectedResponse = "good one"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.men.id)
        data = json.dumps({ "description" :  "good one" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['description']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_slug(self) -> None:
        expectedResponse = "men"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.men.id)
        data = json.dumps({ "slug" : "abcd" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['slug']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_parent(self) -> None:
        expectedResponse = "Object with name=Clothes does not exist."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.men.id)
        data = json.dumps({ "parent" : "Clothes" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['parent'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_child(self) -> None:
        expectedResponse = "Women"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.topwear.id)
        data = json.dumps({ "parent" : "Women" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['parent']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_name_with_empty_input(self) -> None:
        expectedResponse = "This field may not be blank."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.men.id)
        data = json.dumps({ "name" : "" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['name'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_id(self) -> None:
        expectedResponse = "Unable to find category with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        data = json.dumps({ "name" : "" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_existing_name_and_parent(self) -> None:
        expectedResponse = "The fields name, parent must make a unique set."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.topwear.id)
        data = json.dumps({ "name" : "Footwear", "parent" : "Men" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_same_name_and_no_parent(self) -> None:
        expectedResponse = "The fields name, parent must make a unique set."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.men.id)
        data = json.dumps({ "name" : "men", "parent" : None })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)