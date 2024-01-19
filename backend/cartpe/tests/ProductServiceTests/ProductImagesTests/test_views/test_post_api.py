from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, Image
from auth_service.models import User

# Global variables
SAMPLE_IMAGE_1 = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"

# Initialize the APIClient app
client = APIClient()

class PostImageTest(APITestCase):
    """ Test module for POST request for ProductImageAPIView API """

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

    def test_with_valid_data(self) -> None:
        expectedStatusCode = status.HTTP_201_CREATED

        url = self.get_url('product', self.product.id)
        data = { 'image' : SAMPLE_IMAGE_1, 'is_featured' : True }
        response = client.post(url, data)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_image_field(self) -> None:
        expectedResponse = "This field is required."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', self.product.id)
        data = { 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = str(response.data['image'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_invalid_image(self) -> None:
        expectedResponse = "This field may not be blank."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', self.product.id)
        data = { 'image' : "", 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = str(response.data['image'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_missing_featured_field(self) -> None:
        expectedResponse = "This field may not be null."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', self.product.id)
        data = { 'image' : SAMPLE_IMAGE_1 }
        response = client.post(url, data)
        receivedResponse = str(response.data['is_featured'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_true_value_for_is_featured_field(self) -> None:
        self.imageObj = Image.objects.create(image=SAMPLE_IMAGE_1, is_featured=True, product=self.product)
        expectedResponse = "is_featured=True cannot be set as there exists a featured image for productId " + str(self.product.id)
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', self.product.id)
        data = { 'image' : SAMPLE_IMAGE_1, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = str(response.data['message'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_empty_params(self) -> None:
        expectedResponse = "Please make sure query params are sent in the format ?product=<id>."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url()
        data = { 'image' : SAMPLE_IMAGE_1, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_characters_in_params(self) -> None:
        expectedResponse = "Please enter a valid integer for product id."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', 'abc')
        data = { 'image' : SAMPLE_IMAGE_1, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_empty_value_in_params(self) -> None:
        expectedResponse = "Please enter a valid integer for product id."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url('product', '')
        data = { 'image' : SAMPLE_IMAGE_1, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_product_in_params(self) -> None:
        expectedResponse = "Unable to find product with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url('product', 1000)
        data = { 'image' : SAMPLE_IMAGE_1, 'is_featured' : True }
        response = client.post(url, data)
        receivedResponse = str(response.data['message'])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)
