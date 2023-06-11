from django.urls import path
from . import views

urlpatterns = [
    path('routes', views.RoutesAPIView.as_view(), name="auth-routes"),
    path('register', views.RegisterUserAPIView.as_view(), name="register")
]