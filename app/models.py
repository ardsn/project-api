from __future__ import annotations

from .utils import validate_cpf, standardize_numeric_string, standardize_email
from typing import Iterable
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'state'],
                name='unique_city_by_state'
            )
        ]
        ordering = ['name']

    def __str__(self):
        return f"{self.name}/{self.state}"


class Business(models.Model):
    CATEGORY_CHOICES = {
        "C1": "clínica médica",
        "C2": "clínica de psicologia",
        "C3": "clínica de estética",
        "C4": "clínica odontológica",
        "C5": "salão de beleza",
        "C6": "clínica de nutrição",
        "C7": "estúdio de arquitetura",
    }

    name = models.CharField(max_length=70, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    country = models.CharField(max_length=50, default='Brasil', editable=False)
    state = models.CharField(max_length=2)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100)
    public_phone = models.CharField(max_length=15)
    restricted_phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    schedule = models.JSONField()
    closed_on_holidays = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'state', 'city', 'category'],
                name='unique_business_by_category',
            )
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get unique states from the City model
        from django.db import connection
        
        # Check if the City table exists in the database
        if connection.introspection.table_names() and 'app_city' in connection.introspection.table_names():
            from django.db.models import F
            # Get unique states
            unique_states: Iterable[str] = City.objects.values_list('state', flat=True).distinct().order_by('state')
            
            # Create dynamic choices
            choices = [(state, state) for state in unique_states]
            
            # Update the state field with the choices
            self._meta.get_field('state').choices = choices

    
    def __str__(self):
        return f"{self.name} | {self.category} | {self.city}/{self.state}"


    def save(self, **kwargs):
        self.name = self.name.title()
        self.public_phone = standardize_numeric_string(self.public_phone)
        self.restricted_phone = standardize_numeric_string(self.restricted_phone)
        self.email = standardize_email(self.email)
        super().save(**kwargs)



class Customer(models.Model):
    SOURCE_CHOICES = [
        ("whatsapp", "whatsapp"),
        ("website", "website")
    ]

    name = models.CharField(max_length=80)
    birth_date = models.DateField(blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registration_source = models.CharField(
        max_length=50,
        choices=SOURCE_CHOICES,
        editable=False
    )
    cpf = models.CharField(
        max_length=11,
        validators=[validate_cpf],
        unique=True
    )
    email = models.EmailField(max_length=60, blank=True, null=True)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_opt_in = models.BooleanField(default=False)

    def save(self, **kwargs):
        self.name = self.name.replace(" ", "").title()
        self.registration_source = self.registration_source.lower()
        self.email = standardize_email(self.email)
        # Remove non numeric characters
        self.phone = standardize_numeric_string(self.phone)
        self.cpf = standardize_numeric_string(self.cpf)
        super().save(**kwargs)


class Service(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'name'],
                name='unique_business_service'
            )
        ]


    def __str__(self):
        return f"{self.business.name} | {self.name}"

    def save(self, **kwargs):
        self.name = self.name.capitalize()
        super().save(**kwargs)


# # TODO: Finish the model
# class Calendar(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     business = models.ForeignKey(Business, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     date = models.DateTimeField()
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)


class Professional(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    speciality = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    schedule = models.JSONField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['business', 'name'],
                name='unique_business_professional'
            )
        ]

    def save(self, **kwargs):
        self.email = standardize_email(self.email)
        self.speciality = self.speciality.capitalize()
        self.name = self.name.title()
        # Remove non numeric characters
        self.phone = standardize_numeric_string(self.phone)
        super().save(**kwargs)
