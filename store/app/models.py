from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Наименование')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    category = models.ForeignKey('Category', related_name='products', on_delete=models.PROTECT,
                                 verbose_name='Категория')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Последнее изменение')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['created']


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class ContactReason(models.Model):
    name = models.CharField(max_length=150, db_index=True, verbose_name='Причина обращения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Причина обращения'
        verbose_name_plural = 'Причины обращения'
        ordering = ['id']


class Contact(models.Model):
    client_name = models.CharField(max_length=255, verbose_name='Имя клиента')
    reason = models.ForeignKey('ContactReason', related_name='reasons', on_delete=models.PROTECT,
                               verbose_name='Причина обращения')
    content = models.TextField(blank=True, verbose_name='Текст обращения')
    email = models.EmailField(max_length=255, verbose_name='Email')
    order_number = models.CharField(max_length=255, default='не указан', verbose_name='Номер заказа')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    request_granted = models.BooleanField(default=False, verbose_name='Статус обращения')

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
        ordering = ['created']


class Order(models.Model):
    login = models.CharField(max_length=50, verbose_name='Пользователь', default='Без имени')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Последнее изменение')
    status = models.ForeignKey('OrderStatus', related_name='order_status', on_delete=models.PROTECT,
                               verbose_name='Статус заказа', default=1)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created',)

    def __str__(self):
        return '{}'.format(self.pk)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.PROTECT, verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='Цена за шт.')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.pk)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'


class OrderStatus(models.Model):
    status = models.CharField(max_length=255, verbose_name='Статус заказа')

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'

