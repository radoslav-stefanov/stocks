from django import forms

from .models import Portfolio, StockTransaction

class CreatePortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = '__all__'

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = '__all__'