import os
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, Image
from io import BytesIO
from PIL import Image as img

# Initialize the APIClient app
client = APIClient()

class PostImageTest(APITestCase):
    """ Test module for POST request for ProductImageAPIView API """

    def create_valid_image(self):
        image_file = BytesIO()
        image = img.new('RGBA', size=(50, 50), color=(155, 0, 0))
        image.save(image_file, 'png')
        image_file.name = 'test_image.png'
        image_file.seek(0)
        return image_file

    def create_invalid_image(self):
        """ We are not creating and saving the image but just creating a binary object, thus making it an empty file. """
        image_file = BytesIO()
        image_file.name = 'test_image.png'
        image_file.seek(0)
        return image_file

    def get_url(self, paramKey=None, paramValue=None):
        if paramKey is None and paramValue is None:
            url = reverse('images')
        else:
            url = reverse('images') + f"?{paramKey}={paramValue}"
        return url

    def setUp(self) -> None:
        self.product = Product.objects.create(name="pixel 7", description="good product", price=50000, stock_count=10)
        self.myImage = None
        self.imageObj = None

    def test_with_valid_data(self) -> None:
        self.myImage = self.create_valid_image()
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url('product', self.product.id)
        data = { 'image' : self.myImage, 'is_featured' : True }
        response = client.post(url, data)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_image_field(self) -> None:
        expectedResponse = "No file was submitted."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', self.product.id)
        data = { 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = str(response.data['image'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_invalid_image(self) -> None:
        self.myImage = self.create_invalid_image()
        expectedResponse = "The submitted file is empty."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', self.product.id)
        data = { 'image' : self.myImage, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = str(response.data['image'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_featured_field(self) -> None:
        self.myImage = self.create_valid_image()
        expectedResponse = "This field may not be null."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', self.product.id)
        data = { 'image' : self.myImage }
        response = client.post(url, data)
        receivedResponse = str(response.data['is_featured'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_true_value_for_is_featured_field(self) -> None:
        self.myImage = self.create_valid_image()
        self.sampleImage = SimpleUploadedFile("test_image.jpg", b"binary data for image", content_type="image/jpeg")
        self.imageObj = Image.objects.create(image=self.sampleImage, is_featured=True, product=self.product)
        expectedResponse = "is_featured=True cannot be set as there exists a featured image for productId " + str(self.product.id)
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', self.product.id)
        data = { 'image' : self.myImage, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = str(response.data['message'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_empty_params(self) -> None:
        self.myImage = self.create_valid_image()
        expectedResponse = "Please make sure query params are sent in the format ?product=<id>."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = { 'image' : self.myImage, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_characters_in_params(self) -> None:
        self.myImage = self.create_valid_image()
        expectedResponse = "Please enter a valid integer for product id."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', 'abc')
        data = { 'image' : self.myImage, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_empty_value_in_params(self) -> None:
        self.myImage = self.create_valid_image()
        expectedResponse = "Please enter a valid integer for product id."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', '')
        data = { 'image' : self.myImage, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_product_in_params(self) -> None:
        self.myImage = self.create_valid_image()
        expectedResponse = "Unable to find product with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url('product', 1000)
        data = { 'image' : self.myImage, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = str(response.data['message'])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def tearDown(self):
        if self.imageObj is not None:
            self.imageObj.image.delete()

        if self.myImage is not None and os.path.isfile(self.myImage.name):
            os.remove(self.myImage.name)