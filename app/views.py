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

from rest_framework import permissions, viewsets

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    permission_classes = [permissions.IsAuthenticated]


class AvailableDayViewSet(viewsets.ModelViewSet):
    queryset = AvailableDay.objects.all()
    serializer_class = AvailableDaySerializer
    permission_classes = [permissions.IsAuthenticated]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

