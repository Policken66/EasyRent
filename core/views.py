from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from .forms import UserRegisterForm, PropertyCreateForm, ViewingRequestForm, RentalAgreementForm
from .models import Property, ViewingRequest, RentalAgreement
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import threading
from concurrent.futures import ThreadPoolExecutor

import logging

logger = logging.getLogger(__name__)
executor = ThreadPoolExecutor(max_workers=5)

def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user) # Автоматический вход
            return redirect('core:home')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})


def property_list(request):
    sort_by = request.GET.get('sort', 'price')  # Получаем параметр сортировки, по умолчанию 'price'

    if sort_by == 'price':
        properties = Property.objects.order_by('price')  # Сортировка по цене (по возрастанию)
    elif sort_by == '-price':
        properties = Property.objects.order_by('-price')  # Сортировка по цене (по убыванию)
    elif sort_by == 'area':
        properties = Property.objects.order_by('area')  # Сортировка по метражу (по возрастанию)
    elif sort_by == '-area':
        properties = Property.objects.order_by('-area')  # Сортировка по метражу (по убыванию)
    else:
        properties = Property.objects.all()  # Без сортировки
    return render(request, 'core/property_list.html', {'properties': properties})

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyCreateForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.realtor = request.user
            property.save()
            return redirect('core:realtor_properties')  # Перенаправляем на список недвижимости
    else:
        form = PropertyCreateForm()
    return render(request, 'core/property_create.html', {'form': form})

@login_required
def viewing_request(request, property_id):
    property_instance = Property.objects.get(id=property_id) 
    
    if request.method == 'POST':
        form = ViewingRequestForm(request.POST)
        if form.is_valid():
            # Создаем новый запрос на просмотр
            viewing_request = form.save(commit=False)
            viewing_request.user = request.user
            viewing_request.property = property_instance
        
            viewing_request.status = 'pending'
            viewing_request.save()
            return redirect('core:property_list')  # Перенаправляем на список недвиж
    else:
        form = ViewingRequestForm()

    return render(request, 'core/viewing_request.html', {'form': form, 'property': property_instance})

@login_required
def my_viewing_requests(request):
    # Получаем все запросы текущего пользователя
    viewing_requests = ViewingRequest.objects.filter(user=request.user)
    return render(request, 'core/my_viewing_requests.html', {'viewing_requests': viewing_requests})

@login_required
def create_rental_agreement(request, request_id):
    viewing_request = get_object_or_404(ViewingRequest, id=request_id, realtor=request.user)
    
    # Проверяем, что запрос подтверждён
    if viewing_request.status != 'confirmed':
        return HttpResponseForbidden("Вы можете создать договор только для подтверждённых запросов.")

    if request.method == 'POST':
        form = RentalAgreementForm(request.POST)
        if form.is_valid():
            rental_agreement = form.save(commit=False)
            rental_agreement.viewing_request = viewing_request
            rental_agreement.realtor = request.user
            rental_agreement.tenant = viewing_request.user
            rental_agreement.save()
            return redirect('core:realtor_rental_agreements') 
    else:
        form = RentalAgreementForm()

    return render(request, 'core/create_rental_agreement.html', {
        'form': form, 
        'viewing_request': viewing_request
    })

@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def my_rental_agreements(request):
    agreements = RentalAgreement.objects.filter(viewing_request__user=request.user).exclude(status='pending_sent')
    return render(request, 'core/my_rental_agreements.html', {'agreements': agreements})

@login_required
def confirm_rental_agreements(request, agreement_id):
    
    agreement = get_object_or_404(RentalAgreement, id=agreement_id)

    if agreement.status == 'sent':
        agreement.status = 'pending_confirmed'
        agreement.save()
    return redirect('core:my_rental_agreements')


@login_required
def realtor_properties(request):
    properties = Property.objects.filter(realtor=request.user)
    return render(request, 'core/realtor_properties.html', {'properties': properties})

@login_required
def realtor_viewing_requests(request):
    viewing_requests = ViewingRequest.objects.filter(realtor=request.user)
    return render(request, 'core/realtor_viewing_requests.html', {'viewing_requests': viewing_requests})

@login_required
def confirm_viewing_requests(request, viewing_request_id):

    viewing_request = get_object_or_404(ViewingRequest, id=viewing_request_id)

    # Меняем статус записи на "подтверждена"
    if viewing_request.status == 'pending':
        viewing_request.status = 'confirmed'
        viewing_request.save()

    subject='Подтверждение запроса на просмотр'  # Тема письма
    message=f'Здравствуйте, {viewing_request.user.username} # ваш запрос на просмотр недвижимости был подтвержден.',  # Тело письма
    #recipient=[viewing_request.user.email]  # Получатель
    recipient=['komlev.artem.02@mail.ru']  # Получатель
    #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient])
    #send_mail('Django mail', 'This e-mail was sent with Django.', settings.DEFAULT_FROM_EMAIL, ['komlev.artem.02@mail.ru'], fail_silently=False)
    #send_async_email(subject, message, recipient) # Ассинхронная функция для отправки email
     # Запускаем отправку письма в отдельном потоке
    threading.Thread(target=send_async_email, args=(subject, message, recipient)).start()

    return redirect('core:realtor_viewing_requests')

@login_required
def cancel_viewing_requests(request, viewing_request_id):

    viewing_request = get_object_or_404(ViewingRequest, id=viewing_request_id)

    # Меняем статус записи на "подтверждена"
    if viewing_request.status == 'confirmed':
        viewing_request.status = 'pending'
        viewing_request.save()
    
    return redirect('core:realtor_viewing_requests')

@login_required
def realtor_rental_agreements(request):
    agreements = RentalAgreement.objects.filter(realtor=request.user)
    return render(request, 'core/realtor_rental_agreements.html', {'agreements': agreements})

@login_required
def realtor_sent_agreements(request, agreement_id):
    agreement = get_object_or_404(RentalAgreement, id=agreement_id)

    if agreement.status == 'pending_sent':
        agreement.status = 'sent'
        agreement.save()
    
    return redirect('core:realtor_rental_agreements')

@login_required
def realtor_cancel_sent_agreements(request, agreement_id):
    agreement = get_object_or_404(RentalAgreement, id=agreement_id)

    if agreement.status == 'sent' or agreement.status == 'confirmed':
        agreement.status = 'pending_sent'
        agreement.save()
    
    return redirect('core:realtor_rental_agreements')

@login_required
def realtor_confirm_rental_agreements(request, agreement_id):
    agreement = get_object_or_404(RentalAgreement, id=agreement_id)

    if agreement.status == 'pending_confirmed':
        agreement.status = 'confirmed'
        agreement.save()

    return redirect('core:realtor_rental_agreements')


def send_async_email(subject, message, recipient_email):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Email отправителя (берётся из настроек)
            [recipient_email],           # Список получателей
            fail_silently=False          # Если ошибка, то выбрасывать исключение
        )
        print(f"Email отправлен: {recipient_email}")
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")