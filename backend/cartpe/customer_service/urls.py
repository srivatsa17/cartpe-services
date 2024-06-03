from django.urls import path
from . import views

urlpatterns = [
    path('contact-us', views.ContactUsAPIView.as_view(), name="contact_us"),
]