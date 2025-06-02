from .models import (
    City,
    Business,
    Customer,
    Service,
    Professional,
    AvailableDay,
    Appointment
)
from .serializers import (
    CitySerializer,
    BusinessSerializer,
    CustomerSerializer,
    ServiceSerializer,
    ProfessionalSerializer,
    AvailableDaySerializer,
    AppointmentSerializer
)

from rest_framework import viewsets

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer  


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer 


class AvailableDayViewSet(viewsets.ModelViewSet):
    queryset = AvailableDay.objects.all()
    serializer_class = AvailableDaySerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


