from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = Client()

class PostBrandTest(APITestCase):
    """ Test module for POST request for BrandAPIView API """

    def get_url(self):
        url = reverse('brands')
        return url

    def setUp(self) -> None:
        self.validData = { "name" : "Google", "description" : "Amazing" }
        self.dataWithExistingName = self.validData

    def test_with_valid_data(self) -> None:
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url()
        data = json.dumps(self.validData)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_name(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "description" : "Amazing" })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['name'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_description(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps({ "name" : "Google" })
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['description'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_same_name(self) -> None:
        expectedResponse = "Brand '%s' already exists and cannot be created or updated again." % self.validData['name']
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = json.dumps(self.validData)
        client.post(url, data = data, content_type = CONTENT_TYPE)
        response = client.post(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)