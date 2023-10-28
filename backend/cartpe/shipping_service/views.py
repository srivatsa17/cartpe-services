from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from shipping_service.models import Country, Address, UserAddress
from shipping_service.serializers import CountrySerializer, AddressSerializer, UserAddressSerializer

class CountryAPIView(generics.GenericAPIView):
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()

    def get(self, request):
        countries = self.get_queryset()
        serializer = self.serializer_class(countries, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class AddressAPIView(generics.GenericAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()

    def get(self, request):
        addresses = self.get_queryset()
        serializer = self.serializer_class(addresses, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserAddressAPIView(generics.GenericAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        user = self.get_object()
        return UserAddress.objects.filter(user = user)

    def get(self, request):
        user_addresses = self.get_queryset()
        serializer = self.serializer_class(user_addresses, many = True)
        return Response(serializer.data)

    def post(self, request):
        address_serializer = AddressSerializer(data = request.data.get('address'))
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid() and address_serializer.is_valid():
            # Save the address first
            address = address_serializer.save()
            # Now set the address and user and save the user address
            serializer.validated_data['address'] = address
            serializer.validated_data['user'] = self.get_object()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAddressByIdAPIView(generics.GenericAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return UserAddress.objects.get(id = id, user = self.request.user)
        except UserAddress.DoesNotExist:
            response = { "message" : "Unable to find user address with id " + str(id) }
            raise NotFound(response)

    def put(self, request, id):
        user_address = self.get_object(id)

        serializer = self.serializer_class(instance = user_address, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user_address = self.get_object(id)
        # Delete the associated address instance.
        address = user_address.address
        address.delete()
        # Delete the user address instance.
        user_address.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)