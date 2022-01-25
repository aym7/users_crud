from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Customer
        fields = [
            'id', 'creator', 'first_name', 'last_name', 'iban'
        ]

    def validate(self, data):
        """Custom validation for iban, first and last name
        """
        if not data["iban"].isalnum():
            raise serializers.ValidationError('IBAN can only contain alpha-numeric characters.')
        if not data["first_name"].isalpha() or not data["last_name"].isalpha():
            raise serializers.ValidationError('First and last name can only contain alphabetic character.')
        return data


class UserSerializer(serializers.ModelSerializer):
    # As it is a reverse relationship on the User model, won't be included by default.
    # Therefore, must explicitely create it.
    # TODO: See to include the list of customers related to a given user?
    # customers = serializers.PrimaryKeyRelatedField(many=True, queryset=Customer.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username']
