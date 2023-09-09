from django.shortcuts import render
from . forms import CreatePortfolioForm
from .models import Stocks
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, 'stocks/index.html')

def create_portfolio(request):
    form=CreatePortfolioForm()
    context = {'form': form}

    if request.method == 'POST':
        portfolio_name = request.POST.get('portfolio_name')
        portfolio_description = request.POST.get('portfolio_description')

        stock = Stocks()

        stock.portfolio_name = portfolio_name
        stock.portfolio_description = portfolio_description

        stock.save()

        return HttpResponseRedirect(reverse("portfolio", kwargs={'id': stock.pk}))

    return render(request, 'stocks/create-portfolio.html', context)

def portfolio_detail(request, id):
    return render(request, 'stocks/portfolio-detail.html', {})