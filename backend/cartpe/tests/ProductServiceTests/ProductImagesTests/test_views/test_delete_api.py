from django.test import Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from product_service.models import Product, Image

# Initialize the APIClient app
client = Client()

class DeleteImageTest(APITestCase):
    """ Test module for DELETE request for ProductImageByIdAPIView API """

    def get_url(self, imageId):
        url = reverse('image_by_id', kwargs = {'id' : imageId})
        return url

    def setUp(self) -> None:
        self.product = Product.objects.create(name = "pixel 7", description = "good product", price = 50000, stock_count = 10)
        self.sampleImage = SimpleUploadedFile("test_image1.jpg", b"binary data for image", content_type="image/jpeg")
        self.image1 = Image.objects.create(image=self.sampleImage, is_featured=True, product=self.product)

    def test_with_existing_id(self) -> None:
        expectedStatusCode = status.HTTP_204_NO_CONTENT

        url = self.get_url(self.image1.id)
        response = client.delete(url)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_id(self) -> None:
        expectedResponse = "Unable to find image with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        response = client.delete(url)
        receivedResponse = str(response.data['message'])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def tearDown(self) -> None:
        self.sampleImage.close()
        self.image1.image.delete()