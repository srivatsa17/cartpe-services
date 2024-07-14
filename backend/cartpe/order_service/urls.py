from django.urls import path
from . import views

urlpatterns = [
    path("order-routes", views.RoutesAPIView.as_view(), name="order_routes"),
    path("razorpay", views.RazorPayOrderAPIView.as_view(), name="razorpay_orders"),
    path("", views.OrderAPIView.as_view(), name="orders"),
    path("<int:id>", views.OrderByIdAPIView.as_view(), name="order_by_id"),
]
