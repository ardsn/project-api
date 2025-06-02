from rest_framework import serializers
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


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = '__all__'


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
        