from django.contrib import admin
from .models import Manufacturer, Product, Customer, Order, OrderItem, Warehouse


admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Warehouse)