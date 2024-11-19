from django.contrib.auth.models import AbstractUser
from django.db import models

# Модель пользователя с ролями
class User(AbstractUser):
    ADMIN = 'admin'
    CLIENT = 'client'
    ROLE_CHOICES = [
        (ADMIN, 'Администратор'),
        (CLIENT, 'Клиент'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=CLIENT,
    )

    def __str__(self):
        return self.username

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

    def __str__(self):
        return self.title