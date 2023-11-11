from django.test import TestCase
from shipping_service.models import Country

class CountryModelTest(TestCase):
    def setUp(self) -> None:
        Country.objects.create(name = "India")

    def test_str_is_equal_to_title(self):
        country = Country.objects.get(name__iexact = "India")
        expectedResponse = country.name
        receivedResponse = str(country)

        self.assertEqual(receivedResponse, expectedResponse)