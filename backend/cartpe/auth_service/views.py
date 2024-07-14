from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from auth_service.serializers import (
    RegisterUserSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    GoogleLoginSerializer,
    GoogleRegisterSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    DeactivateAccountSerializer,
    EditProfileSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordConfirmSerializer,
)
from auth_service.tasks import send_verification_email_task, send_reset_password_email_task
from auth_service.routes import routes


# Create your views here.
class RoutesAPIView(generics.GenericAPIView):
    queryset = routes

    def get(self, request):
        return Response(self.get_queryset())


class RegisterUserAPIView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Get the email from serializer and use it to send email for email verification.
            user_email = serializer.validated_data["email"]
            send_verification_email_task.delay(user_email=user_email)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleRegisterAPIView(generics.GenericAPIView):
    serializer_class = GoogleRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmailAPIView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            user.is_verified = True
            user.save()
            response = {
                "message": "Email Verified Successfully",
                "isEmailVerified": user.is_verified,
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginAPIView(generics.GenericAPIView):
    serializer_class = GoogleLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            refresh_token = RefreshToken(serializer.validated_data["refresh_token"])
            refresh_token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data, context={"user": user})
        if serializer.is_valid():
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            response = {"message": "Password updated successfully."}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeactivateAccountAPIView(generics.GenericAPIView):
    serializer_class = DeactivateAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            refresh_token = RefreshToken(serializer.validated_data["refresh_token"])
            refresh_token.blacklist()
            user.is_active = False
            user.save()
            response = {"message": "Account deactivated successfully."}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfileAPIView(generics.GenericAPIView):
    serializer_class = EditProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request):
        user = self.get_object()
        serializer = self.serializer_class(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = self.get_object()
        serializer = self.serializer_class(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRequestAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            # Get the email from serializer and use it to send email for password reset.
            user_email = serializer.validated_data["email"]
            send_reset_password_email_task.delay(user_email=user_email)

            response = {"message": "Password reset link has been sent to the provided email."}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = {"message": "Password reset successful."}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
