from django.shortcuts import render
from . forms import CreatePortfolioForm
from .models import Portfolio
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def index(request):
    todos=Portfolio.objects.all()
    context = {'portfolio': portfolio}
    return render(request, 'portfolio/index.html', context)

def create_portfolio(request):
    form=CreatePortfolioForm()
    context = {'form': form}

    if request.method == 'POST':
        portfolio_name = request.POST.get('portfolio_name')
        portfolio_description = request.POST.get('portfolio_description')

        stock = portfolio()

        stock.portfolio_name = portfolio_name
        stock.portfolio_description = portfolio_description

        stock.save()

        return HttpResponseRedirect(reverse("portfolio-detail", kwargs={'id': stock.pk}))

    return render(request, 'portfolio/create-portfolio.html', context)

def portfolio_detail(request, id):
    return render(request, 'portfolio/portfolio-detail.html', {})
