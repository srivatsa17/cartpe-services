from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json
from shipping_service.models import Country, Address, UserAddress
from auth_service.models import User

CONTENT_TYPE = 'application/json'

# Initialize the APIClient app
client = APIClient()

class PutUserAddressByIdTest(APITestCase):
    """ Test module for PUT request for UserAddressByIdAPIView API """

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

        self.validData = {
            "name": "test_user_updated",
            "alternate_phone": "1234567890",
            "type": "Home",
            "is_default": True,
            "address": {
                "line1" : "abc",
                "line2" : "def",
                "city" : "pqr",
                "state" : "xyz",
                "country" : "India",
                "pin_code" : "123244"
            }
        }

    def test_with_valid_data(self) -> None:
        expectedStatusCode = status.HTTP_200_OK
        expectedResponse = "test_user_updated"

        url = self.get_url(self.user_address.id)
        data = json.dumps(self.validData)
        response = client.put(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data["name"]

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_nonexisting_id(self) -> None:
        expectedResponse = "Unable to find user address with id 1000"
        expectedStatusCode = status.HTTP_404_NOT_FOUND

        url = self.get_url(1000)
        data = json.dumps(self.validData)
        response = client.put(url, data = data, content_type = CONTENT_TYPE)
        receivedResponse = response.data['message']
        receivedStatusCode = response.status_code

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)

    def test_with_empty_value(self) -> None:
        expectedResponse = "This field may not be blank."
        expectedStatusCode = status.HTTP_400_BAD_REQUEST

        url = self.get_url(self.user_address.id)
        data = json.dumps({ "name": "" })
        response = client.put(url, data = data, content_type = CONTENT_TYPE)
        receivedStatusCode = response.status_code
        receivedResponse = response.data["name"][0]

        self.assertEqual(receivedResponse, expectedResponse)
        self.assertEqual(receivedStatusCode, expectedStatusCode)