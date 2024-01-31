from rest_framework import serializers
from shipping_service.models import Country, Address, UserAddress
from auth_service.models import User

class CountrySerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    created_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")

    class Meta:
        model = Country
        fields = ['id', 'name', 'created_at', 'updated_at']

    def validate(self, attrs):
        countryName = attrs.get('name', '')
        isCountryFound = Country.objects.filter(name__iexact = countryName).exists()

        if isCountryFound:
            raise serializers.ValidationError({
                "message" : "Country '" + countryName + "' already exists and cannot be created again."
            })

        return super().validate(attrs)

    def create(self, validated_data):
        country = Country.objects.create(**validated_data)
        return country

class AddressSerializer(serializers.ModelSerializer):
    line1 = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    line2 = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    city = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    state = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    country = serializers.SlugRelatedField(slug_field = 'name', queryset = Country.objects.all())
    pin_code = serializers.CharField(min_length = 6, max_length = 6, allow_blank = False, trim_whitespace = True)
    created_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")

    class Meta:
        model = Address
        fields = ['id', 'line1', 'line2', 'city', 'state', 'country', 'pin_code', 'created_at', 'updated_at']

class UserAddressSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length = 1, max_length = 255, allow_blank = False, trim_whitespace = True)
    user = serializers.SlugRelatedField(slug_field = 'email', read_only = True)
    address = AddressSerializer()
    alternate_phone = serializers.CharField(min_length = 10, max_length = 10, allow_blank = False, trim_whitespace = True)
    type = serializers.ChoiceField(choices=[("Home", "Home"), ("Work", "Work"), ("Other", "Other")])
    is_default = serializers.BooleanField(allow_null = False)
    created_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")
    updated_at = serializers.DateTimeField(read_only = True, format="%d %b %Y, %H:%M")

    class Meta:
        model = UserAddress
        fields = ['id', 'name', 'user', 'address', 'alternate_phone', 'type', 'is_default', 'created_at', 'updated_at']

    def validate(self, attrs):
        is_default_address = attrs.get('is_default', '')
        user = self.context.get('user', '')

        # If is_default = True and there exists an entry in table which already is the default address,
        # we update the table entry by setting is_default = False and saving the new entry with is_default = True.
        if is_default_address and UserAddress.objects.filter(is_default = True, user = user).exists():
            user_address_obj = UserAddress.objects.get(is_default = True)
            user_address_obj.is_default = False
            user_address_obj.save()

        return attrs

    def update(self, instance, validated_data):
        """
        The update method is written to update the address model fields from UserAddressByIdAPIView.
        Since address data is a nested object in request data, we need to update individual fields of address model
        in the following way.
        """
        # Get the address object from validated request data.
        address_data = validated_data.pop('address')
        # Get the serialized data of address object from UserAddressSerializer.
        address = instance.address

        # Update the fields of address model and save it.
        for attr, value in address_data.items():
            setattr(address, attr, value)
        address.save()  # Save the updated address instance.

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()  # Save the updated user address instance.

        return instance