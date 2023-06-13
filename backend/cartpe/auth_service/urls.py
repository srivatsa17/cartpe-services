from django.urls import path
from . import views

urlpatterns = [
    path('routes', views.RoutesAPIView.as_view(), name="auth-routes"),
    path('register', views.RegisterUserAPIView.as_view(), name="register"),
    path('verify-email', views.VerifyUserEmailAPIView.as_view(), name="verify-email"),
    path('login', views.LoginAPIView.as_view(), name="login"),
]