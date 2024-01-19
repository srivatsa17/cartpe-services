from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, Image
from product_service.serializers import ProductImageSerializer
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

class GetAllImagesTest(APITestCase):
    """ Test module for GET request for ProductImageAPIView API """

    def get_url(self, paramKey=None, paramValue=None):
        if paramKey is None and paramValue is None:
            url = reverse('images')
        else:
            url = reverse('images') + f"?{paramKey}={paramValue}"
        return url

    def setUp(self) -> None:
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name="Canon 80D", description="good product", price=50000, stock_count=10)
        self.sampleImage = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"
        self.imageInstance1 = Image.objects.create(image=self.sampleImage, is_featured=True, product=self.product)
        self.imageInstance2 = Image.objects.create(image=self.sampleImage, is_featured=False, product=self.product)

    def test_with_valid_params(self) -> None:
        images = Image.objects.filter(product = self.product)
        serializer = ProductImageSerializer(images, many = True)
        expectedResponse = serializer.data
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url('product', self.product.id)
        response = client.get(url)
        receivedResponse = response.data
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_empty_params(self) -> None:
        expectedResponse = "Please make sure query params are sent in the format ?product=<id>."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        response = client.get(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_characters_in_params(self) -> None:
        expectedResponse = "Please enter a valid integer for product id."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', 'abc')
        response = client.get(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_empty_value_in_params(self) -> None:
        expectedResponse = "Please enter a valid integer for product id."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', '')
        response = client.get(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_product_in_params(self) -> None:
        expectedResponse = "Unable to find product with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url('product', 1000)
        response = client.get(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

class GetImageByIdTest(APITestCase):
    """ Test module for GET request for ProductImageByIdAPIView API """

    def get_url(self, imageId):
        url = reverse('image_by_id', kwargs = {'id' : imageId})
        return url

    def setUp(self) -> None:
        self.product = Product.objects.create(name="Canon 80D", description="good product", price=50000, stock_count=10)
        self.sampleImage = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"
        self.imageInstance1 = Image.objects.create(image=self.sampleImage, is_featured=True, product=self.product)
        self.imageInstance2 = Image.objects.create(image=self.sampleImage, is_featured=False, product=self.product)

    def test_with_valid_image_id(self) -> None:
        image = Image.objects.get(id = self.imageInstance1.id)
        serializer = ProductImageSerializer(image, many = False)
        expectedResponse = serializer.data
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.imageInstance1.id)
        response = client.get(url)
        receivedResponse = response.data
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_invalid_image_id(self) -> None:
        expectedResponse = "Unable to find image with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        response = client.get(url)
        receivedResponse = str(response.data['message'])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)