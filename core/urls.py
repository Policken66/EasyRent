from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('property/<int:property_id>/request/', views.viewing_request, name='viewing_request'),
    path('my_requests/', views.my_viewing_requests, name='my_viewing_requests'),
    path('my_rental_agreements/', views.my_rental_agreements, name='my_rental_agreements'),
    path('rental_agreement/<int:request_id>/', views.create_rental_agreement, name='create_rental_agreement'),

    path('profile/', views.profile, name='profile'),
]