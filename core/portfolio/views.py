from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum
from django.contrib import messages
from .forms import CreatePortfolioForm, StockTransactionForm
from .models import Portfolio, StockTransaction

import yfinance as yf
from decimal import Decimal

# Cache
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

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

        messages.add_message(request, messages.SUCCESS, 'Portfolio created successfully.')

        return HttpResponseRedirect(reverse("portfolio-detail", kwargs={'id': portfolio.pk}))

    return render(request, 'portfolio/create-portfolio.html', context)

@receiver(post_save, sender=StockTransaction)
def clear_portfolio_cache(sender, **kwargs):
    portfolio_id = kwargs['instance'].portfolio.id
    cache_key = f'portfolio_{portfolio_id}_summary'
    cache.delete(cache_key)

def add_stock_transaction(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    form = StockTransactionForm()
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            stock_transaction = form.save(commit=False)
            stock_transaction.portfolio = portfolio
            stock_transaction.save()
            
            # Clear cache for this portfolio
            clear_portfolio_cache(sender=StockTransaction, instance=stock_transaction)
            
            return HttpResponseRedirect(reverse("portfolio-detail", kwargs={'id': portfolio_id}))
    context = {'form': form}

    messages.add_message(request, messages.SUCCESS, 'Stock transaction added successfully.')

    return render(request, 'portfolio/add_stock_transaction.html', context)

def portfolio_detail(request, id):
    portfolio = get_object_or_404(Portfolio, pk=id)
    transactions = StockTransaction.objects.filter(portfolio=portfolio)
    
    # Try to get data from cache
    summary = cache.get(f'portfolio_{id}_summary')
    
    if summary is None:
        # Data not in cache, fetch and store
        summary = transactions.values('ticker').annotate(
            total_shares=Sum('shares'),
            total_cost=Sum('cost')
        )
        
        tickers = [stock['ticker'] for stock in summary]
        ticker_str = ' '.join(tickers)
        data = yf.download(ticker_str, period="1d", group_by='ticker')
        
        for stock in summary:
            stock_data = data[stock['ticker']]
            if not stock_data.empty:
                stock['current_price'] = stock_data['Close'].iloc[-1]
            else:
                stock['current_price'] = 'N/A'
        
        # Store data in cache for 5 minutes
        cache.set(f'portfolio_{id}_summary', summary, 300)
    
    # Calculate P&L for each stock
    for stock in summary:
        if stock['current_price'] != 'N/A':
            stock['PnL'] = (Decimal(stock['current_price']) - Decimal(stock['total_cost'] / stock['total_shares'])) * stock['total_shares']
        else:
            stock['PnL'] = 'N/A'
    
    context = {
        'portfolio': portfolio,
        'summary': summary,
        'transactions_url': reverse("transactions-list", kwargs={'id': id})
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

    messages.add_message(request, messages.SUCCESS, 'Stock transaction added successfully.')

    return render(request, 'portfolio/edit_stock_transaction.html', context)

def delete_stock_transaction(request, portfolio_id, id):
    transaction = get_object_or_404(StockTransaction, id=id)
    transaction.delete()
    return redirect('portfolio-detail', id=portfolio_id)

def edit_portfolio(request, id):
    portfolio = get_object_or_404(Portfolio, id=id)
    form = CreatePortfolioForm(instance=portfolio)
    
    if request.method == 'POST':
        form = CreatePortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()

            messages.add_message(request, messages.SUCCESS, 'Portfolio updated successfully.')

            return redirect('home')
    
    context = {'form': form}
    return render(request, 'portfolio/edit_portfolio.html', context)

def delete_portfolio(request, id):
    portfolio = get_object_or_404(Portfolio, id=id)
    if request.method == 'POST':
        portfolio.delete()
        messages.add_message(request, messages.SUCCESS, 'Portfolio deleted successfully.')
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'portfolio/portfolio-delete.html', {'portfolio': portfolio})

def delete_transaction(request, portfolio_id, id):
    transaction = get_object_or_404(StockTransaction, id=id)
    if request.method == 'POST':
        transaction.delete()
        messages.add_message(request, messages.SUCCESS, 'Transaction deleted successfully.')
        return HttpResponseRedirect(reverse('portfolio-detail', kwargs={'id': portfolio_id}))
    return render(request, 'portfolio/transaction-delete.html', {'cancel_url': reverse('portfolio-detail', kwargs={'id': portfolio_id})})

def fetch_spy_price_on_date(date):
    spy = yf.Ticker("SPY")
    historical_data = spy.history(period="1d", start=date, end=date)
    return historical_data['Close'][0] if not historical_data.empty else None

def transactions_list(request, id):
    portfolio = get_object_or_404(Portfolio, pk=id)
    #transactions = StockTransaction.objects.filter(portfolio=portfolio)
    transactions = StockTransaction.objects.filter(portfolio_id=id)

    for transaction in transactions:
        # Fetch current SPY price (you can use yfinance or any other method)
        current_spy_price = fetch_spy_price_on_date(transaction.date)
        transaction.performance_vs_spy = (current_spy_price - transaction.spy_price_at_purchase) / transaction.spy_price_at_purchase * 100

        # Calculate performance vs SPY
        if current_spy_price and transaction.spy_price_at_purchase:
            transaction.performance_vs_spy = ((current_spy_price - transaction.spy_price_at_purchase) / transaction.spy_price_at_purchase) * 100

    context = {
        'portfolio': portfolio,
        'transactions': transactions
    }
    return render(request, 'portfolio/transactions_list.html', context)