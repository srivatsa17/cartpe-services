from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from shipping_service.models import Country, Address, UserAddress
from auth_service.models import User

# Initialize the APIClient app
client = APIClient()

class DeleteUserAddressByIdTest(APITestCase):
    """ Test module for DELETE request for UserAddressByIdAPIView API """

    def get_url(self, user_address_id):
        url = reverse("user_address_by_id", kwargs = { "id" : user_address_id })
        return url

    def setUp(self):
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        client.force_authenticate(user = self.user)

        self.country = Country.objects.create(name = "India")
        self.address = Address.objects.create(
            building = "abc", area = "def", city = "pqr", state = "xyz", country = self.country, pin_code = "123244"
        )
        self.user_address = UserAddress.objects.create(
            name = "test_user", user = self.user, address = self.address, alternate_phone = "1234567890",
            type = "Home", is_default = False
        )

    def test_delete_with_existing_id(self):
        url = self.get_url(self.user_address.id)
        response = client.delete(url)

        self.assertIsNone(response.data)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_with_nonexisting_id(self):
        url = self.get_url(1000)
        response = client.delete(url)

        self.assertEqual("Unable to find user address with id 1000", response.data["message"])
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
