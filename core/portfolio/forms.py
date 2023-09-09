from django import forms
from . models import Portfolio

class CreatePortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = "__all__"
