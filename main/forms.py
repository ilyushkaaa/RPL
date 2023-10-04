import hashlib

from django import forms
from .models import Match, Goal, Footballer, Team, Fan
from django.forms import NumberInput, DateTimeInput, DateInput  # Импортируйте модели данных


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['id', 'team_home', 'team_guest', 'referee', 'date', 'is_over']
        # fields = '__all__'
        widgets = {
            "id": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID'
            }),
            "date": DateInput(attrs={
                'type': 'date'
            }),

        }


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['id', 'footballer', 'minute', 'match']


class FootballerForm(forms.ModelForm):
    # position = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Footballer
        fields = '__all__'
        widgets = {
            "id": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ID'
            }),
            "birthday": DateInput(attrs={
                'type': 'date'

            }),

        }


class FanRegistrationForm(forms.ModelForm):
    class Meta:
        model = Fan
        fields = ['first_name', 'last_name', 'birthday', 'favourite_team', 'password', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'birthday': 'Дата рождения',
            'favourite_team': 'Любимая команда',
            'password': 'Пароль',
            'email': 'Email'
        }
        widgets = {

            "birthday": DateInput(attrs={
                'type': 'date'

            }),

        }


class FanLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                fan = Fan.objects.get(email=email)

                if not fan.check_password(password):
                    raise forms.ValidationError('Неверный пароль')
            except Fan.DoesNotExist:
                raise forms.ValidationError('Пользователь с таким email не существует')

        return cleaned_data


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Fan
        fields = ['first_name', 'last_name', 'favourite_team']
        labels = {
            'first_name': 'Имя',  # Новая подпись для поля first_name
            'last_name': 'Фамилия',  # Новая подпись для поля last_name
            'favourite_team': 'Любимая команда',  # Новая подпись для поля favourite_team
        }
