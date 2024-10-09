from django.db import models
from django.contrib.auth.models import User


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Производитель")
    country = models.CharField(max_length=255, verbose_name="Страна")

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name


class Warehouse(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название склада")
    location = models.CharField(max_length=255, verbose_name="Местоположение")

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение товара")
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")

    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        verbose_name="Производитель")

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        verbose_name="Склад"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Customer(models.Model):
    phone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    address = models.CharField(max_length=255, blank=True, verbose_name="Адрес")

    user = models.OneToOneField(
        User, # Тут использовал встроенную
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )

    favorites = models.ManyToManyField(
        Product,
        related_name='favorited_by',
        verbose_name="Избранные товары",
        blank=True
    )

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"

    def __str__(self):
        return self.user.username


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    complete = models.BooleanField(default=False, verbose_name="Завершен")

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Покупатель"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ {self.id} от {self.customer.user.username}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Заказ"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        return self.quantity * self.product.price