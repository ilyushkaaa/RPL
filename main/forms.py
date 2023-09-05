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
                'type': 'date'
            }),


        }


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['id', 'footballer', 'minute', 'match']


class FootballerForm(forms.ModelForm):
    #position = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

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
