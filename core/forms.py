from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Property, ViewingRequest, RentalAgreement

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

        labels = {
            'title': 'Название',
            'description': 'Описание',
            'area': 'Площадь',
            'price': 'Цена',
            'location': 'Адрес',
            'status': 'Статус',
        }

class ViewingRequestForm(forms.ModelForm):
    class Meta:
        model = ViewingRequest
        fields = ['property', 'viewing_time']

    viewing_time = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата просмотра"
    )

    property = forms.ModelChoiceField(
        queryset=Property.objects.all(),
        label="Недвижимость",
    )

    # Для автозаполнения пользователя
    def __init__(self, *args, **kwargs):
        user = kwargs.get('user')
        super(ViewingRequestForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.user = user

# Форма для создания договора
class RentalAgreementForm(forms.ModelForm):
    class Meta:
        model = RentalAgreement
        fields = ['viewing_request', 'start_date', 'end_date', 'rent_price']

    viewing_request = forms.ModelChoiceField(
        queryset=ViewingRequest.objects.all(),
        label="Успешные просмотры"
    )


    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата заезда"
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата выезда"
    )

    rent_price = forms.DecimalField(
        label ="Стоимость аренды",
    )

    


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Пре-фильтрация только подтвержденных запросов
        self.fields['viewing_request'].queryset = self.fields['viewing_request'].queryset.filter(status='confirmed')
