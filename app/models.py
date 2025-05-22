from __future__ import annotations

from .utils import (
    standardize_numeric_string,
    standardize_email,
    Source,
    AppointmentStatus,
    BusinessCategory
)
from .validators import (
    validate_price,
    validate_date,
    validate_datetime,
    validate_cpf,
    validate_duration,
    validate_phone_number
)
from django.db import models


SOURCE_CHOICES = [
    (source.name, source.value) for source in Source
]


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'state'],
                name='unique_name_state'
            )
        ]

    def __str__(self):
        return f"{self.name}/{self.state}"

    def save(self, **kwargs):
        # Run all validations for the model
        self.full_clean()
        super().save(**kwargs)


class Business(models.Model):
    CATEGORY_CHOICES = [
        (category.name, category.value) for category in BusinessCategory
    ]

    name = models.CharField(max_length=70)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    country = models.CharField(max_length=50, default='Brasil', editable=False)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100)
    public_phone = models.CharField(max_length=15, validators=[validate_phone_number])
    restricted_phone = models.CharField(max_length=15, validators=[validate_phone_number])
    email = models.EmailField(max_length=100)
    schedule = models.JSONField()
    closed_on_holidays = models.BooleanField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'city', 'category'],
                name='unique_name_category_city'
            )
        ]

    def __str__(self):
        return f"{self.name} | {self.category} | {self.city}/{self.state}"

    def save(self, **kwargs):
        # Standardize the data for database
        self.name = self.name.title()
        self.public_phone = standardize_numeric_string(self.public_phone)
        self.restricted_phone = standardize_numeric_string(self.restricted_phone)
        self.email = standardize_email(self.email)
        # Run all validations for the model
        self.full_clean()
        super().save(**kwargs)



class Customer(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    birth_date = models.DateField(blank=True, null=True)
    registration_source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        editable=False
    )
    cpf = models.CharField(
        max_length=14,
        validators=[validate_cpf]
    )
    email = models.EmailField(max_length=60, blank=True, null=True)
    phone = models.CharField(max_length=15, validators=[validate_phone_number])
    is_active = models.BooleanField(default=True)
    is_opt_in = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'cpf'],
                name='unique_customer_business'
            )
        ]

    def save(self, **kwargs):
        # Standardize the data for database
        self.name = self.name.title()
        self.registration_source = self.registration_source.upper()
        self.email = standardize_email(self.email)
        # Remove non numeric characters
        self.phone = standardize_numeric_string(self.phone)
        self.cpf = standardize_numeric_string(self.cpf)
        # Run all validations for the model
        self.full_clean()
        super().save(**kwargs)


class Service(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[validate_price]
    )
    duration = models.DurationField(validators=[validate_duration])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'name'],
                name='unique_business_name'
            )
        ]

    def __str__(self):
        return f"{self.business.name} | {self.name}"

    def save(self, **kwargs):
        # Standardize the data for database
        self.name = self.name.capitalize()
        # Run all validations for the model
        self.full_clean()
        super().save(**kwargs)


class Professional(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    cpf = models.CharField(
        max_length=14,
        validators=[validate_cpf]
    )
    speciality = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    schedule = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'cpf'],
                name='unique_business_professional'
            )
        ]

    def save(self, **kwargs):
        # Standardize the data for database
        self.email = standardize_email(self.email)
        self.speciality = self.speciality.capitalize()
        self.name = self.name.title()
        # Remove non numeric characters
        self.phone = standardize_numeric_string(self.phone)
        self.cpf = standardize_numeric_string(self.cpf)
        # Run all validations for the model
        self.full_clean()
        super().save(**kwargs)


class AvailableDay(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    # If the professional is not set, the day is available for all professionals
    professional = models.ForeignKey(
        Professional,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    date = models.DateField(validators=[validate_date])
    # If the blocked start and end are not set, the day is available for all hours
    blocked_start_time = models.TimeField(blank=True, null=True)
    blocked_end_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'professional', 'date'],
                name='unique_business_professional_date',
                nulls_distinct=False
            )
        ]

    def save(self, **kwargs):
        # Run all validations for the model
        self.full_clean()
        super().save(**kwargs)


class Appointment(models.Model):
    STATUS_CHOICES = [
        (status.name, status.value) for status in AppointmentStatus
    ]

    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    datetime = models.DateTimeField(validators=[validate_datetime])
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=AppointmentStatus.SCHEDULED.name
    )
    source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'professional', 'datetime', 'customer', 'service', 'status'],
                name='unique_business_professional_datetime_customer_service_status'
            ) 
        ]

    def save(self, **kwargs):
        # Standardize the data for database
        self.status = self.status.upper()
        self.source = self.source.upper()
        # Run all validations for the model
        self.full_clean()
        super().save(**kwargs)