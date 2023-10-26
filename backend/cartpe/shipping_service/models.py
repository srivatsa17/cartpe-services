from django.db import models
from auth_service.models import User

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length = 255, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.name

class Address(models.Model):
    line1 = models.CharField(max_length = 255, null = False, blank = False)
    line2 = models.CharField(max_length = 255, null = False, blank = False)
    city = models.CharField(max_length = 255, null = False, blank = False)
    state = models.CharField(max_length = 255, null = False, blank = False)
    country = models.ForeignKey(to = Country, on_delete = models.CASCADE, null = False, blank = False, related_name = 'address')
    pin_code = models.CharField(max_length = 255, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        address = "%s, %s, %s, %s, %s, %s" % (self.line1, self.line2, self.city, self.state, self.country, self.pin_code)
        return address
    
class UserAddress(models.Model):
    ADDRESS_TYPE_CHOICES = (
        (1, "Home"),
        (2, "Work")
    )
    name = models.CharField(max_length = 255, null = False, blank = False)
    user = models.ForeignKey(to = User, on_delete = models.CASCADE, null = False, blank = False, related_name = 'user_address')
    address = models.ForeignKey(to = Address, on_delete = models.CASCADE, null = False, blank = False, related_name = 'user_address')
    alternate_phone = models.CharField(max_length = 10, null = False, blank = False)
    type = models.CharField(null = False, blank = False, choices = ADDRESS_TYPE_CHOICES)
    is_default = models.BooleanField(null = False, blank = False, default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.name