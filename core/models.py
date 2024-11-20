from django.contrib.auth.models import AbstractUser
from django.db import models

# Модель пользователя с ролями
class User(AbstractUser):

    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('client', 'Клиент'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='client',
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Модель объявления о недвижимости
class PropertyListing(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Квартира'),
        ('house', 'Дом'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    area = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('available', 'Свободно'), ('rented', 'Сдано')])
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)

    @staticmethod
    def filter_listings(status=None, property_type=None, min_price=None, max_price=None):
        queryset = PropertyListing.objects.all()

        if status:
            queryset = queryset.filter(status=status)
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def __str__(self):
        return self.title