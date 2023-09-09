from django import forms
from . models import AddTransaction

class AddTransactionForm(forms.ModelForm):
    class Meta:
        model = AddTransaction