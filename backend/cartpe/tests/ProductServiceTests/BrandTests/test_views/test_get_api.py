from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from product_service.models import Brand
from product_service.serializers import BrandSerializer

# Initialize the APIClient app
client = Client()

class GetAllBrandsTest(APITestCase):
    """ Test module for GET request for BrandAPIView API """

    def get_url(self):
        url = reverse('brands')
        return url

    def setUp(self) -> None:
        Brand.objects.create(name = "Apple", description = "ok brand")
        Brand.objects.create(name = "Google", description = "good brand")

    def test_valid_data(self) -> None:
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many = True)
        expectedResponse = serializer.data
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url()
        response = client.get(url)
        receivedResponse = response.data
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)


class GetBrandByIdTest(APITestCase):
    """ Test module for GET request for BrandByIdAPIView API """

    def get_url(self, brandId):
        url = reverse('brand_by_id', kwargs = { 'id' : brandId })
        return url

    def setUp(self) -> None:
        self.apple = Brand.objects.create(name = "apple", description = "ok brand")
        self.google = Brand.objects.create(name = "google", description = "good brand")

    def test_with_valid_id(self) -> None:
        brand = Brand.objects.get(id = self.google.pk)
        serializer = BrandSerializer(brand, many = False)
        expectedResponse = serializer.data
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.google.id)
        response = client.get(url)
        receivedResponse = response.data
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test__with_invalid_id(self) -> None:
        expectedResponse = "Unable to find brand with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        response = client.get(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)