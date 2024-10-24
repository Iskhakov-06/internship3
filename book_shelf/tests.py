from django.urls import reverse
from django.test import TestCase
from .models import Product
from .factories import ProductFactory, ManufacturerFactory, WarehouseFactory


class ProductViewTest(TestCase):

    def setUp(self):
        self.product = ProductFactory()

    # Тест ListView
    def test_product_list_view(self):
        url = reverse('product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertEqual(response.context['products'].count(), Product.objects.count())
        print(response)

    # Тест DetailView
    def test_product_detail_view(self):
        url = reverse('product_detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    # Тест CreateView
    def test_product_create_view(self):
        manufacturer = ManufacturerFactory()
        warehouse = WarehouseFactory()
        data = {
            'name': 'New Product',
            'price': 150.0,
            'manufacturer': manufacturer.pk,
            'warehouse': warehouse.pk,
        }
        url = reverse('product_create')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 2)

    # Тест UpdateView
    def test_product_update_view(self):
        data = {
            'name': 'Updated Product',
            'price': 200.0,
            'manufacturer': self.product.manufacturer.pk,
            'warehouse': self.product.warehouse.pk,
        }
        url = reverse('product_update', kwargs={'pk': self.product.pk})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    # Тест DeleteView
    def test_product_delete_view(self):
        url = reverse('product_delete', kwargs={'pk': self.product.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 0)
