from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from product_service.models import Product, Image
from auth_service.models import User

# Global variables
SAMPLE_IMAGE_1 = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"
SAMPLE_IMAGE_2 = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_2.webp"

# Initialize the APIClient app
client = APIClient()

class UpdateImageTest(APITestCase):
    """ Test module for PATCH request for ProductImageByIdAPIView API """

    def get_url(self, imageId):
        url = reverse('image_by_id', kwargs = {'id' : imageId})
        return url

    def setUp(self) -> None:
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.product = Product.objects.create(name="Canon 80D", description="good product", price=50000, stock_count=10)
        self.image1 = Image.objects.create(image=SAMPLE_IMAGE_1.replace("\'", "\""), is_featured=True, product=self.product)

    def test_with_valid_image_id(self) -> None:
        expectedResponse = SAMPLE_IMAGE_2
        expectedStatusCode = status.HTTP_200_OK

        url = self.get_url(self.image1.id)
        data = { "image" : SAMPLE_IMAGE_2, "is_featured" : False }
        response = client.patch(url, data)

        receivedResponse = response.data['image']
        receivedStatusCode = response.status_code

        self.assertIn(expectedResponse, receivedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_invalid_image_id(self) -> None:
        expectedResponse = "Unable to find image with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        data = { "image" : SAMPLE_IMAGE_1, "is_featured" : False }
        response = client.patch(url, data)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_empty_image_url(self) -> None:
        expectedResponse = "This field may not be blank."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.image1.id)
        data = { 'image' : "", 'is_featured' : True }
        response = client.patch(url, data)
        receivedResponse = str(response.data['image'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_true_value_for_is_featured_field(self) -> None:
        expectedResponse = "is_featured=True cannot be set as there exists a featured image for productId " + str(self.product.id)
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.image1.id)
        data = { 'image' : SAMPLE_IMAGE_1, 'is_featured' : True }
        response = client.patch(url, data)
        receivedResponse = str(response.data['message'][0])
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)