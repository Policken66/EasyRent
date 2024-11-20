from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Property, ViewingRequest

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'client'
        if commit:
            user.save()
        return user

class PropertyCreateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'area', 'location', 'price', 'status']

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'price': forms.NumberInput(attrs={'min': 0}),
            'area': forms.NumberInput(attrs={'min': 0}),
        }

class ViewingRequestForm(forms.ModelForm):
    class Meta:
        model = ViewingRequest
        fields = ['property', 'viewing_time']

    viewing_time = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата просмотра"
    )

    # Для автозаполнения пользователя
    def __init__(self, *args, **kwargs):
        user = kwargs.get('user')
        super(ViewingRequestForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.user = user