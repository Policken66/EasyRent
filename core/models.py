from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.mail import send_mail

# Модель пользователя с ролями
class User(AbstractUser):

    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('realtor', 'Риелтор'),
        ('client', 'Клиент'),   
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='client',
    )

    def get_icon(self):
        # Если роль пользователя 'admin', то возвращаем иконку admin.png
        if self.role == 'admin':
            return f"Icons/15.png"
        else:
            # Для всех остальных пользователей выбираем иконку по остаточному значению от деления на 20
            icon_number = self.id % 16  # Получаем остаток от деления id на 20
            return f"Icons/{icon_number + 1}.png"  # Иконка будет иметь номер от 1 до 20

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)

    #Метод для отправки сообщения о подтверждении на просмотр
    def send_confirmation_email(self, viewing_request):
        subject = 'Подтверждение на просмотр'
        message = (
            f'Здравствствуйте, {self.username}!\n\n'
            f"Ваш запрос на просмотр объекта недвижимости {viewing_request.property.title} был"
            f"Дата просмотра: {viewing_request.viewing_time.strftime('%d-%m-%Y')}\n"
            f"Местоположение: {viewing_request.property.location}\n\n"
            f"Цена: {viewing_request.property.price} руб.\n\n"
            f"С уважением,\nEasy Rent."
        )
        recipient = self.email
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])

        
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
    realtor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties',
        limit_choices_to={'role': 'realtor'},
        null=True,  # На случай, если нужно оставить недвижимость без риелтора
        blank=True
    )
    
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
    realtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewing_requests_as_realtor', verbose_name="Риелтор", null=True)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    viewing_time = models.DateField() # Время, когда клиент хочет посмотреть объект 

    def __str__(self):
        return f'Запрос на просмотр {self.property.title} от {self.user.username}'
    
# Модель договора
class RentalAgreement(models.Model):
    STATUS_CHOICES = [
        ('pending_sent', 'Ожидает отправления'),
        ('sent', 'Отправлено'),
        ('pending_confirmed', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
    ]

    viewing_request = models.OneToOneField(ViewingRequest, on_delete=models.CASCADE)
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_agreements')
    realtor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='realtor_agreements', verbose_name="Риелтор", null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)
    signed_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending_sent')

    def __str__(self):
        return f"Договор аренды: {self.viewing_request.property.title} - {self.tenant.username}"
    