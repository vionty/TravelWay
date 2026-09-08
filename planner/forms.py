from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Trip, Destination, Place


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Электронная почта'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]


class PasswordResetUsernameForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=150
    )


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'title',
            'start_date',
            'end_date',
            'budget',
            'status',
            'notes',
        ]

        labels = {
            'title': 'Название поездки',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'budget': 'Бюджет',
            'status': 'Статус поездки',
            'notes': 'Заметки',
        }

        widgets = {
            'start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            ),
            'notes': forms.Textarea(
                attrs={'rows': 4}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['start_date'].input_formats = [
            '%Y-%m-%d'
        ]

        self.fields['end_date'].input_formats = [
            '%Y-%m-%d'
        ]

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        budget = cleaned_data.get('budget')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                'Дата окончания не может быть раньше даты начала.'
            )

        if budget is not None and budget < 0:
            raise forms.ValidationError(
                'Бюджет не может быть отрицательным.'
            )

        return cleaned_data


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination

        fields = [
            'country',
            'city',
        ]

        labels = {
            'country': 'Страна',
            'city': 'Город',
        }


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place

        fields = [
            'name',
            'description',
            'address',
            'visited',
        ]

        labels = {
            'name': 'Название места',
            'description': 'Описание',
            'address': 'Адрес',
            'visited': 'Посещено',
        }

        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 4}
            ),
        }
