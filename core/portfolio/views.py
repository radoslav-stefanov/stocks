from django.shortcuts import render
from . forms import CreatePortfolioForm
from . forms import StockTransactionForm
from .models import Portfolio, StockTransaction
from . models import Portfolio
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    portfolios = Portfolio.objects.all()
    count_all_portfolios = portfolios.count()
    context = {'portfolios': portfolios, 'count_all_portfolios': count_all_portfolios}

    return render(request, 'portfolio/index.html', context)

def create_portfolio(request):
    form=CreatePortfolioForm()
    context = {'form': form}

    if request.method == 'POST':
        portfolio_name = request.POST.get('portfolio_name')
        portfolio_description = request.POST.get('portfolio_description')

        portfolio = Portfolio()

        portfolio.portfolio_name = portfolio_name
        portfolio.portfolio_description = portfolio_description

        portfolio.save()

        return HttpResponseRedirect(reverse("portfolio-detail", kwargs={'id': portfolio.pk}))

    return render(request, 'portfolio/create-portfolio.html', context)

def portfolio_detail(request, id):
    return render(request, 'portfolio/portfolio-detail.html', {})

def add_stock_transaction(request, portfolio_id):
    form = StockTransactionForm()
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("portfolio-detail", kwargs={'id': portfolio_id}))
    context = {'form': form}
    return render(request, 'portfolio/add_stock_transaction.html', context)

def portfolio_detail(request, id):
    portfolio=get_object_or_404(Portfolio, pk=id)
    
    portfolio = Portfolio.objects.get(pk=id)
    summary = StockTransaction.objects.values('ticker').annotate(
        total_shares=Sum('shares'),
        total_cost=Sum('cost')
    ).filter(portfolio=portfolio)
    
    context = {
        'portfolio': portfolio,
        'summary': summary
    }
    return render(request, 'portfolio/portfolio-detail.html', context)

def portfolio_delete(request, id):
    portfolio = Portfolio.objects.get(pk=id)
    context = {'portfolio': portfolio}

    portfolio.delete()
    return render(request, 'portfolio/portfolio-delete.html', context)