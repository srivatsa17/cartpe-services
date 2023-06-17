from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from auth_service.serializers import (
    RegisterUserSerializer, EmailVerificationSerializer, LoginSerializer, LogoutSerializer,
    ChangePasswordSerializer
)
from auth_service.tasks import send_verification_email_task
from auth_service.routes import routes

# Create your views here.
class RoutesAPIView(generics.GenericAPIView):
    queryset = routes

    def get(self, request):
        return Response(self.get_queryset())

class RegisterUserAPIView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()

            # Get the email from serializer and use it to send email for email verification.
            user_email = serializer.validated_data['email']
            send_verification_email_task.delay(user_email = user_email)

            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class VerifyUserEmailAPIView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def patch(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            user.is_verified = True
            user.save()
            response = {
                "message" : "Email Verified Successfully",
                "isEmailVerified" : user.is_verified
            }
            return Response(response, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            refresh_token = RefreshToken(serializer.validated_data['refresh_token'])
            refresh_token.blacklist()
            return Response(status = status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(data = request.data, context = {'user' : user})
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            response = { "message" : "Password updated successfully." }
            return Response(response, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)