from django.test import TestCase
from shipping_service.models import Country, Address


class AddressModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="India")
        self.address = Address.objects.create(
            building="abc",
            area="def",
            city="pqr",
            state="xyz",
            country=self.country,
            pin_code="123244",
        )

    def test_str_is_equal_to_title(self):
        self.assertEqual(
            "%s, %s, %s, %s, %s, %s"
            % (
                self.address.building,
                self.address.area,
                self.address.city,
                self.address.state,
                self.address.country,
                self.address.pin_code,
            ),
            str(Address.objects.get(id=self.address.id)),
        )
