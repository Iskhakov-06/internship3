from rest_framework import serializers

from .models import Product, Manufacturer, Warehouse


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
