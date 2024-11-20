from django.contrib import admin
from .models import Property, ViewingRequest, RentalAgreement

# Register your models here.
admin.site.register(Property)
admin.site.register(ViewingRequest)
admin.site.register(RentalAgreement)