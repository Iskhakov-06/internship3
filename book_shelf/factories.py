import factory
from random import choice
from .models import Product, Manufacturer, Warehouse

countries = ['Russia', 'USA', 'Africa', 'Iran', 'China']

locations = ['New York', 'Moscow', 'Ufa', 'Beijing']


class ManufacturerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Manufacturer

    name = factory.Sequence(lambda n: f'Manufacturer {n}')

    country = choice(countries)


class WarehouseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Warehouse

    name = factory.Sequence(lambda n: f'Warehouse {n}')
    location = choice(locations)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    price = choice(range(100, 1000))
    manufacturer = factory.SubFactory(ManufacturerFactory)
    warehouse = factory.SubFactory(WarehouseFactory)
