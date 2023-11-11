from django.test import TestCase
from shipping_service.models import Country, Address

class AddressModelTest(TestCase):
    def setUp(self) -> None:
        self.country = Country.objects.create(name = "India")
        self.address = Address.objects.create(
            line1 = "abc", line2 = "def", city = "pqr", state = "xyz", country = self.country,
            pin_code = "123244"
        )

    def test_str_is_equal_to_title(self):
        address = Address.objects.get(id = self.address.id)
        expectedResponse = "%s, %s, %s, %s, %s, %s" % (address.line1, address.line2, address.city, address.state, address.country, address.pin_code)
        receivedResponse = str(address)

        self.assertEqual(receivedResponse, expectedResponse)