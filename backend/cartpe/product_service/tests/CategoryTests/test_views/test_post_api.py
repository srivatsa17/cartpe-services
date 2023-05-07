from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = Client()

class PostCategoryTest(APITestCase):
    """ Test module for POST request for CategoryAPIView API """

    def get_url(self):
        url = reverse('categories')
        return url

    def setUp(self) -> None:
        self.validData = { "name" : "Men", "description" : "Clothing for men", "parent" : None }
        self.subcategory = { "name" : "Topwear", "description" : "Topwear for men", "parent" : "Men" }

    def test_with_valid_data(self) -> None:
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url()
        data = json.dumps(self.validData)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_subcategory(self) -> None:
        initialData = json.dumps(self.validData)
        data = json.dumps(self.subcategory)
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url()
        client.post(url, data = initialData, content_type = CONTENT_TYPE)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_name(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "description" : "Clothing for men", "parent" : None })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['name'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_description(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "name" : "Men", "parent" : None })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['description'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_parent(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "name" : "Men", "description" : "Clothing" })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['parent'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_parent(self) -> None:
        expectedResponse = "Object with name=Men does not exist."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps(self.subcategory)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['parent'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_same_name_and_parent_combination(self) -> None:
        expectedResponse = "The fields name, parent must make a unique set."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps(self.validData)
        client.post(url, data = data, content_type = CONTENT_TYPE)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)