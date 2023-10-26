from django.urls import path
from . import views

urlpatterns = [
    path('countries', views.CountryAPIView.as_view(), name="country"),
    path('address', views.AddressAPIView.as_view(), name="address"),
    path('user-address', views.UserAddressAPIView.as_view(), name="user-address"),
]