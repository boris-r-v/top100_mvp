from django import forms
from .models import Excursion
from django.core.validators import MinLengthValidator

class PasswordForm(forms.Form):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )

class ExcursionForm(forms.ModelForm):
    class Meta:
        model = Excursion
        fields = ['city', 'company', 'full_name', 'email', 'phone', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 (XXX) XXX-XX-XX'}),
        }

class SearchForm(forms.Form):
#    city = forms.CharField(
#        label="Город",
#        required=False,
#        widget=forms.TextInput(attrs={'placeholder': 'Введите город'})
#    )
    city = forms.CharField(
        validators=[MinLengthValidator(2)],
        label="Город",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите город',
            'minlength': '2'
        })
    )
    search_date = forms.DateField(
        label="Дата экскурсии",
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )