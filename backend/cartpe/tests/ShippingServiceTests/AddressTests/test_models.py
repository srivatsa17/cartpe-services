from django.test import TestCase
from shipping_service.models import Country, Address

class AddressModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name = "India")
        self.address = Address.objects.create(
            line1 = "abc", line2 = "def", city = "pqr", state = "xyz", country = self.country, pin_code = "123244"
        )

    def test_str_is_equal_to_title(self):
        self.assertEqual(
            "%s, %s, %s, %s, %s, %s" % (self.address.line1, self.address.line2, self.address.city,
                self.address.state, self.address.country, self.address.pin_code
            ), str(Address.objects.get(id = self.address.id))
        )
