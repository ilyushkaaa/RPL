from django import forms
from .models import Match, Goal, Footballer, Team
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
                'class': 'form-control',
                'placeholder': 'ID'
            }),


        }


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = '__all__'


class FootballerForm(forms.ModelForm):
    class Meta:
        model = Footballer
        fields = '__all__'
