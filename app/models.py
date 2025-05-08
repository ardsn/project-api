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
        return f"{self.name} - {self.state}"


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
    