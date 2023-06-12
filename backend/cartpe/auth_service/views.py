from rest_framework.response import Response
from rest_framework import generics, status
from auth_service.serializers import RegisterUserSerializer, EmailVerificationSerializer
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
            return Response(status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)