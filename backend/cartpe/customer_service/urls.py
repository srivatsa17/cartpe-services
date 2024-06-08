from django.urls import path
from . import views

urlpatterns = [
    path('customer-service-routes', views.RoutesAPIView.as_view(), name="customer_service_routes"),
    path('contact-us', views.ContactUsAPIView.as_view(), name="contact_us"),
]