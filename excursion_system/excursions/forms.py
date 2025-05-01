from django import forms
from .models import Excursion

class PasswordForm(forms.Form):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )

class ExcursionForm(forms.ModelForm):
    class Meta:
        model = Excursion
        fields = ['city', 'company', 'full_name', 'email', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SearchForm(forms.Form):
    search_date = forms.DateField(
        label="Дата экскурсии",
        widget=forms.DateInput(attrs={'type': 'date'})
    )    