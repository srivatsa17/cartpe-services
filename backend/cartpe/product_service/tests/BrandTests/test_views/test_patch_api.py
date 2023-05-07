from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json
from product_service.models import Brand

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = Client()

class UpdateBrandByIdTest(APITestCase):
    """ Test module for PATCH request for BrandByIdAPIView API """

    def get_url(self, brandId):
        url = reverse('brand_by_id', kwargs={'id' : brandId})
        return url

    def setUp(self) -> None:
        self.google = Brand.objects.create(name="Google", description="good brand")

    def test_with_id(self) -> None:
        expectedResponse = self.google.id
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.google.id)
        data = json.dumps({ "id" : 20 })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['id']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_name(self) -> None:
        expectedResponse = "abc"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.google.id)
        data = json.dumps({ "name" : "abc" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['name']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_description(self) -> None:
        expectedResponse = "amazing brand"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.google.id)
        data = json.dumps({ "description" : "amazing brand" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['description']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_slug(self) -> None:
        expectedResponse = "google"
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.google.id)
        data = json.dumps({ "slug" : "abcd" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['slug']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_name_with_empty_input(self) -> None:
        expectedResponse = "This field may not be blank."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.google.id)
        data = json.dumps({ "name" : "" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['name'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_id(self) -> None:
        expectedResponse = "Unable to find brand with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        data = json.dumps({ "name" : "" })
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_same_name(self) -> None:
        expectedResponse = "Brand 'Google' already exists and cannot be created or updated again."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.google.id)
        data = json.dumps({ "name" : "Google"})
        response = client.patch(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message'][0]
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)
