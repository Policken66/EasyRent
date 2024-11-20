from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegisterForm, PropertyCreateForm, ViewingRequestForm, RentalAgreementForm
from .models import Property, ViewingRequest
from django.contrib.auth.decorators import login_required

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
    properties = Property.objects.all()
    return render(request, 'core/property_list.html', {'properties': properties})

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:property_list')  # Перенаправляем на список недвижимости
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
    requests = ViewingRequest.objects.filter(user=request.user)
    return render(request, 'core/my_viewing_requests.html', {'requests': requests})

@login_required
def create_rental_agreement(request, request_id):
    viewing_request = get_object_or_404(ViewingRequest, id=request_id, user=request.user)
     # Обрабатываем форму для создания договора
    if request.method == 'POST':
        form = RentalAgreementForm(request.POST)
        if form.is_valid():
            rental_agreement = form.save(commit=False)
            rental_agreement.viewing_request = viewing_request
            rental_agreement.tenant = request.user
            rental_agreement.save()
            return redirect('core:my_viewing_requests') 

    else:
        form = RentalAgreementForm()

    return render(request, 'core/create_rental_agreement.html', {'form': form, 'viewing_request': viewing_request})