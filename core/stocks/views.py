from django.shortcuts import render
from . forms import CreatePortfolioForm
from .models import Stocks

# Create your views here.

def index(request):
    return render(request, 'stocks/index.html')

def create_portfolio(request):
    form=CreatePortfolioForm()
    context = {'form': form}

    if request.method == 'POST':
        stock_name = request.POST.get('stock_name')
        stock_price = request.POST.get('stock_price')

        stock = Stocks()

        stock.stock_name = stock_name
        stock.stock_price = stock_price

        stock.save()

    return render(request, 'stocks/create-portfolio.html', context)
