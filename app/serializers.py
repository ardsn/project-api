from rest_framework import serializers
from .utils import (
    standardize_numeric_string,
    standardize_email
)
from .models import (
    City,
    Business,
    Customer,
    Service,
    Professional,
    AvailableDay,
    Appointment
)
from typing import Any


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        read_only_fields = ['id', 'name', 'state']

    def create(self, validated_data: dict[str, Any]) -> None:
        raise serializers.ValidationError('This table is read only')
    
    def update(self, instance: City, validated_data: dict[str, Any]) -> None:
        raise serializers.ValidationError('This table is read only')


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

    def to_internal_value(self, data: dict[str, Any] | Any) -> dict[str, Any]:
        """
        Standardize the data BEFORE validation
        """
        # Create a copy to avoid modifying the original
        data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Standardize specific fields for database
        if 'name' in data and data['name']:
            data['name'] = data['name'].title()

        if 'public_phone' in data and data['public_phone']:
            data['public_phone'] = standardize_numeric_string(data['public_phone'])

        if 'restricted_phone' in data and data['restricted_phone']:
            data['restricted_phone'] = standardize_numeric_string(data['restricted_phone'])

        if 'email' in data and data['email']:
            data['email'] = standardize_email(data['email'])

        # Call the parent method with standardized data
        return super().to_internal_value(data)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def to_internal_value(self, data: dict[str, Any] | Any) -> dict[str, Any]:
        """
        Standardize the data before validation
        """
        # Create a copy to avoid modifying the original
        data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Standardize specific fields for database
        if 'name' in data and data['name']:
            data['name'] = data['name'].title()

        if 'registration_source' in data and data['registration_source']:
            data['registration_source'] = data['registration_source'].upper()

        if 'email' in data and data['email']:
            data['email'] = standardize_email(data['email'])

        if 'phone' in data and data['phone']:
            data['phone'] = standardize_numeric_string(data['phone'])

        if 'cpf' in data and data['cpf']:
            data['cpf'] = standardize_numeric_string(data['cpf'])

        # Call the parent method with standardized data
        return super().to_internal_value(data)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

    def to_internal_value(self, data: dict[str, Any] | Any) -> dict[str, Any]:
        """
        Standardize the data before validation
        """
        # Create a copy to avoid modifying the original
        data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Standardize specific fields for database
        if 'name' in data and data['name']:
            data['name'] = data['name'].capitalize()

        # Call the parent method with standardized data
        return super().to_internal_value(data)


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = '__all__'

    def to_internal_value(self, data: dict[str, Any] | Any) -> dict[str, Any]:
        """
        Standardize the data before validation
        """
        # Create a copy to avoid modifying the original
        data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Standardize specific fields for database
        if 'name' in data and data['name']:
            data['name'] = data['name'].title()
        
        if 'email' in data and data['email']:
            data['email'] = standardize_email(data['email'])

        if 'speciality' in data and data['speciality']:
            data['speciality'] = data['speciality'].capitalize()

        if 'phone' in data and data['phone']:
            data['phone'] = standardize_numeric_string(data['phone'])

        if 'cpf' in data and data['cpf']:
            data['cpf'] = standardize_numeric_string(data['cpf'])
            
        # Call the parent method with standardized data
        return super().to_internal_value(data)


class AvailableDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableDay
        fields = '__all__'

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Check if the blocked start time is before the blocked end time.
        If only one of the two times is provided, raise a validation error.
        """
        blocked_start_time = data.get('blocked_start_time')
        blocked_end_time = data.get('blocked_end_time')

        # If both blocked start and end times are provided,
        # check if the start time is before the end time
        if blocked_start_time is not None and blocked_end_time is not None:
            if blocked_start_time >= blocked_end_time:
                raise serializers.ValidationError(
                    'The blocked start time must be before the blocked end time'
                )
        elif blocked_start_time is not None or blocked_end_time is not None:
            raise serializers.ValidationError(
                'Both blocked_start_time and blocked_end_time must be provided together'
            )
        return data
        

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def to_internal_value(self, data: dict[str, Any] | Any) -> dict[str, Any]:
        """
        Standardize the data before validation
        """
        # Create a copy to avoid modifying the original
        data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Standardize specific fields for database
        if 'status' in data and data['status']:
            data['status'] = data['status'].upper()

        if 'source' in data and data['source']:
            data['source'] = data['source'].upper()

        # Call the parent method with standardized data
        return super().to_internal_value(data)
