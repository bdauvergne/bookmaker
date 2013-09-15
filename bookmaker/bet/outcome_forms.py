from django import forms

from . import models

class OutcomeCreateForm(forms.ModelForm):
    class Meta:
        model = models.Outcome
        fields = ('description',)

class BetForm(forms.ModelForm):
    class Meta:
        model = models.Bet
        fields = ('amount',)
