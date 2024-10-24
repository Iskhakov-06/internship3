import django_filters
from django.db.models import Q

from .models import Product


class ProductFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Название товара')
    # description = django_filters.CharFilter(field_name='description', lookup_expr='icontains', label='Описание товара')
    price_range = django_filters.RangeFilter(field_name='price', label='Цена от и до')
    available = django_filters.BooleanFilter(method='filter_available', label='В наличии')
    term = django_filters.CharFilter(method='filter_term',
                                     label='поиск по названию товара ИЛИ по названию производителю')
    warehouse_and_stock = django_filters.CharFilter(method='filter_warehouse_and_stock',
                                                    label='поиск по названию склада И по чтобы был в наличии')

    class Meta:

        model = Product
        # fields = ['name', 'description', 'price_range', 'available']
        fields = ['price_range', 'available', 'term', 'warehouse_and_stock']

    def filter_available(self, queryset, name, value):
        if value is None:
            return queryset
        if value:
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock=0)

    def filter_term(self, queryset, name, value):
        criteria = Q()
        for term in value.split():
            criteria &= Q(name__icontains=term) | Q(manufacturer__name__icontains=term)

        return queryset.filter(criteria).distinct()

    def filter_warehouse_and_stock(self, queryset, name, value):
        criteria = Q()
        for temp in value.split():
            criteria &= Q(warehouse__name__icontains=temp) & Q(stock__gt=0)

        return queryset.filter(criteria).distinct()
