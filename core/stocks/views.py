from django.shortcuts import render
from . forms import AddTransactionForm

# Create your views here.

def index(request):
    return render(request, 'stocks/index.html')

def add_transaction(request):
    form=AddTransactionForm()
    return render(request, 'stocks/add-transaction.html')