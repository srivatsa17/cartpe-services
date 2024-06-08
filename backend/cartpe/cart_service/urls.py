from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartAPIView.as_view(), name="cart"),
    path('<int:id>', views.CartByIdAPIView.as_view(), name="cart_by_id"),
    path('cart-routes', views.RoutesAPIView.as_view(), name="cart_routes"),
]