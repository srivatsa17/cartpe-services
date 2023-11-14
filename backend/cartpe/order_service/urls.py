from django.urls import path
from . import views

urlpatterns = [
    path('razorpay', views.RazorPayOrderAPIView.as_view(), name="razorpay_orders"),
    path('', views.OrderAPIView.as_view(), name="orders"),
]