from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('routes', views.RoutesAPIView.as_view(), name="auth-routes"),
    path('register', views.RegisterUserAPIView.as_view(), name="register"),
    path('verify-email', views.VerifyUserEmailAPIView.as_view(), name="verify-email"),
    path('login', views.LoginAPIView.as_view(), name="login"),
    path('google-login', views.GoogleLoginAPIView.as_view(), name="google-login"),
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('logout', views.LogoutAPIView.as_view(), name="logout"),
    path('change-password', views.ChangePasswordAPIView.as_view(), name="change-password"),
    path('deactivate', views.DeactivateAccountAPIView.as_view(), name="deactivate"),
]