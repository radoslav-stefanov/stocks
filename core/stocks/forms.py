from django import forms
from . models import Stocks

class CreatePortfolioForm(forms.ModelForm):
    class Meta:
        model = Stocks
        fields = "__all__"
