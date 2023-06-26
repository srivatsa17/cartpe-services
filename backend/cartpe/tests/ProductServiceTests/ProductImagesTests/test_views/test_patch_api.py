import os
from django.urls import reverse
from django.test.client import encode_multipart
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, Image
from io import BytesIO
from PIL import Image as img

# Global variables
BOUNDARY = 'BoUnDaRyStRiNg'
MULTIPART_CONTENT = 'multipart/form-data; boundary=%s' % BOUNDARY

# Initialize the APIClient app
client = APIClient()

class UpdateImageTest(APITestCase):
    """ Test module for PATCH request for ProductImageByIdAPIView API """

    def create_valid_image(self):
        image_file = BytesIO()
        image = img.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(image_file, 'png')
        image_file.name = 'test_image2.png'
        image_file.seek(0)
        return image_file

    def create_invalid_image(self):
        """ We are not creating and saving the image but just creating a binary object, thus making it an empty file. """
        image_file = BytesIO()
        image_file.name = 'test_image.png'
        image_file.seek(0)
        return image_file

    def get_url(self, imageId):
        url = reverse('image_by_id', kwargs = {'id' : imageId})
        return url

    def setUp(self) -> None:
        self.product = Product.objects.create(name="pixel 7", description="good product", price=50000, stock_count=10)
        self.sampleImage = SimpleUploadedFile("test_image1.jpg", b"binary data for image", content_type="image/jpeg")
        self.image1 = Image.objects.create(image=self.sampleImage, is_featured=True, product=self.product)
        self.myImage = None

    def test_with_valid_image_id(self) -> None:
        self.myImage = self.create_valid_image()
        expectedResponse = 'test_image2.png'
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.image1.id)
        data = { "image" : self.myImage, 'is_featured' : False }
        encoded_data = encode_multipart(data=data, boundary=BOUNDARY)
        response = client.patch(url, encoded_data, content_type=MULTIPART_CONTENT)
        receivedResponse = response.data['image']
        receivedStatusCode = response.status_code

        self.assertIn(expectedResponse, receivedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_invalid_image_id(self) -> None:
        self.myImage = self.create_valid_image()
        expectedResponse = "Unable to find image with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        data = { "image" : self.myImage, 'is_featured' : False}
        encoded_data = encode_multipart(data=data, boundary=BOUNDARY)
        response = client.patch(url, encoded_data, content_type=MULTIPART_CONTENT)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_invalid_image(self) -> None:
        self.myImage = self.create_invalid_image()
        expectedResponse = "The submitted file is empty."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.image1.id)
        data = { 'image' : self.myImage, 'is_featured' : True }
        encoded_data = encode_multipart(data=data, boundary=BOUNDARY)
        response = client.patch(url, encoded_data, content_type=MULTIPART_CONTENT)
        receivedResponse = str(response.data['image'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_true_value_for_is_featured_field(self) -> None:
        self.myImage = self.create_valid_image()
        expectedResponse = "is_featured=True cannot be set as there exists a featured image for productId " + str(self.product.id)
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.image1.id)
        data = { 'image' : self.myImage, 'is_featured' : True }
        encoded_data = encode_multipart(data=data, boundary=BOUNDARY)
        response = client.patch(url, encoded_data, content_type=MULTIPART_CONTENT)
        receivedResponse = str(response.data['message'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def tearDown(self):
        self.sampleImage.close()
        self.image1.image.delete()
        if self.myImage is not None and os.path.isfile(self.myImage.name):
            os.remove(self.myImage.name)