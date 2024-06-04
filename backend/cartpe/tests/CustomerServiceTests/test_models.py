from django.test import TestCase
from auth_service.models import User
from customer_service.models import ContactUs
from customer_service.constants import CustomerService

class OrderModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email = "testuser@example.com", password = "abcdef")
        self.inquiry = ContactUs.objects.create(
            topic = CustomerService.GENERAL_INQUIRY, comment = "When is the next product sale",
            user = self.user
        )

    def test_str_is_equal_to_title(self):
        self.assertEqual(str(self.inquiry.topic), str(ContactUs.objects.get(id = self.inquiry.id)))
