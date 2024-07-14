from django.test import TestCase
from shipping_service.models import Country


class CountryModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="India")

    def test_str_is_equal_to_title(self):
        self.assertEqual(self.country.name, str(Country.objects.get(name__iexact="India")))
