from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from shipping_service.models import Country, Address, UserAddress
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

class DeleteUserAddressByIdTest(APITestCase):
    """ Test module for DELETE request for UserAddressByIdAPIView API """

    def get_url(self, userAddressId):
        url = reverse('user_address_by_id', kwargs={'id' : userAddressId})
        return url

    def setUp(self) -> None:
        # Creating a user and forcing the authentication.
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.country = Country.objects.create(name = "India")
        self.address = Address.objects.create(
            line1 = "abc", line2 = "def", city = "pqr", state = "xyz", country = self.country,
            pin_code = "123244"
        )
        self.user_address = UserAddress.objects.create(
            name = "test_user",
            user = self.user,
            address = self.address,
            alternate_phone = "1234567890",
            type = "Home",
            is_default = False
        )

    def test_with_existing_id(self) -> None:
        expectedStatusCode = status.HTTP_204_NO_CONTENT

        url = self.get_url(self.user_address.id)
        response = client.delete(url)
        receivedStatusCode = response.status_code

        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_id(self) -> None:
        expectedResponse = "Unable to find user address with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        response = client.delete(url)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)