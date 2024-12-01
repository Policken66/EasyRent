from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
    path('properties/', views.property_list, name='property_list'),
    path('profile/', views.profile, name='profile'),

    # Страницы взаимодествия с недвижимостью
    path('properties/create/', views.property_create, name='property_create'),
    path('property/<int:property_id>/request/', views.viewing_request, name='viewing_request'),
    path('realtor_properties/', views.realtor_properties, name='realtor_properties'),

    # Страницы для профиля пользователя
    path('my_requests/', views.my_viewing_requests, name='my_viewing_requests'),
    path('my_rental_agreements/', views.my_rental_agreements, name='my_rental_agreements'),

    # Работа с договорами со стороны пользователя
    path('rental_agreement/<int:request_id>/', views.create_rental_agreement, name='create_rental_agreement'),
    path('rental_agreement/confirm/<int:agreement_id>/', views.confirm_rental_agreements, name='confirm_rental_agreements'),

    # Работа с запросами на просмотр со стороны риелтора 
    path('realtor_viewing_requests/', views.realtor_viewing_requests, name='realtor_viewing_requests'),
    path('viewing_requests/confirm/<int:viewing_request_id>/', views.confirm_viewing_requests, name='confirm_viewing_requests'),
    path('viewing_requests/cancel/<int:viewing_request_id>/', views.cancel_viewing_requests, name='cancel_viewing_requests'),

    # Работа с договорами со стороны риелтора
    path('realtor_rental_agreements/', views.realtor_rental_agreements, name='realtor_rental_agreements'),
    path('realtor_sent_agreements/<int:agreement_id>/', views.realtor_sent_agreements, name='realtor_sent_agreements'),
    path('realtor_cancel_sent_agreements/<int:agreement_id>/', views.realtor_cancel_sent_agreements, name='realtor_cancel_sent_agreements'),
    path('realtor_confirm_rental_agreements/<int:agreement_id>/', views.realtor_confirm_rental_agreements, name='realtor_confirm_rental_agreements'),
    ]