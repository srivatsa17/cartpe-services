from django.test import TestCase
from shipping_service.models import Country, Address, UserAddress
from auth_service.models import User

class UserAddressModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name = "India")
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        self.address = Address.objects.create(
            building = "abc", area = "def", city = "pqr", state = "xyz", country = self.country, pin_code = "123244"
        )
        self.user_address = UserAddress.objects.create(
            name = "test_user", user = self.user, address = self.address, alternate_phone = "1234567890",
            type = "Home", is_default = False
        )

    def test_str_is_equal_to_title(self):
        self.assertEqual(self.user_address.name, str(UserAddress.objects.get(id = self.user_address.id)))
