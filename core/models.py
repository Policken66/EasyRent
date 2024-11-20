from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

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
class Property(models.Model):
    PROPERTY_STATUS = [
        ('available', 'Свободно'),
        ('rented', 'Сдано'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    area = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=PROPERTY_STATUS, default='available')
    
    def __str__(self):
        return self.title
    
# Модель запроса на просмотр
class ViewingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    viewing_time = models.DateField() # Время, когда клиент хочет посмотреть объект 

    def __str__(self):
        return f'Запрос на просмотр {self.property.title} от {self.user.username}'
    
# Модель договора
class RentalAgreement(models.Model):
    viewing_request = models.OneToOneField(ViewingRequest, on_delete=models.CASCADE)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_agreements')
    start_date = models.DateField()
    end_date = models.DateField()
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    signed_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Договор аренды: {self.viewing_request.property.title} - {self.tenant.username}"