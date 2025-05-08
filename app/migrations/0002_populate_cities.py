from app.utils import fetch_cities
from typing import Any, Iterable
from django.db import migrations



def populate_cities(apps, schema_editor):
    City = apps.get_model('app', 'City')
    
    # Get cities data
    cities_data: Iterable[dict[str, Any]] = fetch_cities()
    
    # Create cities in the database
    for city_data in cities_data:
        city_name = city_data['nome']
        state_uf = city_data['regiao-imediata']['regiao-intermediaria']['UF']['sigla']
        
        if not City.objects.filter(name=city_name, state=state_uf).exists():
            City.objects.create(
                name=city_name,
                state=state_uf
            )

def reverse_populate_cities(apps, schema_editor):
    City = apps.get_model('app', 'City')
    City.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_cities, reverse_code=reverse_populate_cities),
    ] 