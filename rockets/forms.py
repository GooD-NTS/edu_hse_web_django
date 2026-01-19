from django import forms
from .models import Rocket, Cosmodrome, Launch


class RocketForm(forms.ModelForm):
    """Форма для добавления/редактирования ракеты"""
    
    class Meta:
        model = Rocket
        fields = [
            'name', 'manufacturer', 'country', 'rocket_type', 'status',
            'first_flight_year', 'height', 'diameter', 'mass', 'payload_to_leo',
            'stages', 'description'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название ракеты'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Производитель'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Страна'}),
            'rocket_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'first_flight_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Например: 2020', 'min': 1900, 'max': 2100}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Высота в метрах'}),
            'diameter': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Диаметр в метрах'}),
            'mass': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Масса в тоннах'}),
            'payload_to_leo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Полезная нагрузка в кг'}),
            'stages': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество ступеней'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание ракеты'}),
        }


class CosmodromeForm(forms.ModelForm):
    """Форма для добавления/редактирования космодрома"""
    
    class Meta:
        model = Cosmodrome
        fields = ['name', 'country', 'location', 'founded_year', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название космодрома'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Страна'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Местоположение'}),
            'founded_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год основания'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание космодрома'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class LaunchForm(forms.ModelForm):
    """Форма для добавления/редактирования запуска"""
    
    class Meta:
        model = Launch
        fields = [
            'mission_name', 'rocket', 'cosmodrome', 'launch_date',
            'status', 'payload', 'orbit', 'description'
        ]
        widgets = {
            'mission_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название миссии'}),
            'rocket': forms.Select(attrs={'class': 'form-select'}),
            'cosmodrome': forms.Select(attrs={'class': 'form-select'}),
            'launch_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payload': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Полезная нагрузка'}),
            'orbit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Орбита (например: LEO, GTO, SSO)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание миссии'}),
        }


class SearchForm(forms.Form):
    """Форма поиска"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск...',
            'aria-label': 'Поиск'
        })
    )
