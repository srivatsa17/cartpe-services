from django.db import models
from order_service.models import Order

class Payment(models.Model): 
    order = models.ForeignKey(to = Order, on_delete = models.CASCADE, null = False, blank = False, related_name = 'payment')
    total_mrp = models.DecimalField(max_digits = 7, decimal_places = 2, null = False, blank = False)
    total_discount_price = models.DecimalField(max_digits = 7, decimal_places = 2, null = False, blank = False)
    total_selling_price = models.DecimalField(max_digits = 7, decimal_places = 2, null = False, blank = False)
    convenience_fee = models.PositiveSmallIntegerField(null = False, blank = False)
    shipping_fee = models.PositiveSmallIntegerField(null = False, blank = False)
    total_amount = models.DecimalField(max_digits = 7, decimal_places = 2, null = False, blank = False)
    round_off_price = models.DecimalField(max_digits = 7, decimal_places = 2, null = False, blank = False)
    savings_amount = models.DecimalField(max_digits = 7, decimal_places = 2, null = False, blank = False)
    savings_percent = models.DecimalField(max_digits = 7, decimal_places = 2, null = False, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.pk)
