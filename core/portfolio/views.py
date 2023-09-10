from django.shortcuts import render
from . forms import CreatePortfolioForm
from . forms import StockTransactionForm
from .models import Portfolio, StockTransaction
from . models import Portfolio
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
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
    portfolio = get_object_or_404(Portfolio, pk=id)
    transactions = StockTransaction.objects.filter(portfolio=portfolio)
    summary = transactions.values('ticker').annotate(
        total_shares=Sum('shares'),
        total_cost=Sum('cost')
    )
    
    context = {
        'portfolio': portfolio,
        'summary': summary,
        'transactions': transactions
    }
    return render(request, 'portfolio/portfolio-detail.html', context)


def edit_stock_transaction(request, portfolio_id, id):
    transaction = get_object_or_404(StockTransaction, id=id)
    form = StockTransactionForm(instance=transaction)
    
    if request.method == 'POST':
        form = StockTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('portfolio-detail', id=portfolio_id)
    
    context = {'form': form}
    return render(request, 'portfolio/edit_stock_transaction.html', context)

def delete_stock_transaction(request, portfolio_id, id):
    transaction = get_object_or_404(StockTransaction, id=id)
    transaction.delete()
    return redirect('portfolio-detail', id=portfolio_id)
