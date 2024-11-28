from celery import shared_task
from .models import ViewingRequest
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_confirmation_email_task(viewing_request_id):
    try:
        viewing_request = ViewingRequest.objects.get(id=viewing_request_id)
        user = viewing_request.user

        subject = 'Подтверждение на просмотр'
        message = (
            f'Здравствуйте, {user.username}!\n\n'
            f"Ваш запрос на просмотр объекта недвижимости '{viewing_request.property.title}' был подтвержден.\n"
            f"Дата просмотра: {viewing_request.viewing_time.strftime('%d-%m-%Y %H:%M')}\n"
            f"Местоположение: {viewing_request.property.location}\n\n"
            f"Цена: {viewing_request.property.price} руб.\n\n"
            f"С уважением,\nEasy Rent."
        )

        recipient_list = [user.email]

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        return f"Email sent to {user.email} for viewing request {viewing_request.id}"
    except ViewingRequest.DoesNotExist:
        return f"ViewingRequest with id {viewing_request_id} does not exist."