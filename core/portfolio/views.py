from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum
from django.contrib import messages
from .forms import CreatePortfolioForm, StockTransactionForm
from .models import Portfolio, StockTransaction

import yfinance as yf
from decimal import Decimal

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

def add_stock_transaction(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    form = StockTransactionForm()
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        if form.is_valid():
            stock_transaction = form.save(commit=False)
            stock_transaction.portfolio = portfolio
            stock_transaction.save()
            return HttpResponseRedirect(reverse("portfolio-detail", kwargs={'id': portfolio_id}))
    context = {'form': form}

    messages.add_message(request, messages.SUCCESS, 'Stock transaction added successfully.')

    return render(request, 'portfolio/add_stock_transaction.html', context)

def portfolio_detail(request, id):
    portfolio = get_object_or_404(Portfolio, pk=id)
    transactions = StockTransaction.objects.filter(portfolio=portfolio)
    summary = transactions.values('id', 'ticker').annotate(
        total_shares=Sum('shares'),
        total_cost=Sum('cost')
    )

    for stock in summary:
        ticker_symbol = stock.get('ticker', None)
        if ticker_symbol:
            ticker = yf.Ticker(ticker_symbol)
            stock['current_price'] = Decimal(ticker.history(period="1d")['Close'].iloc[0])
            stock['average_price'] = Decimal(stock['total_cost']) / Decimal(stock['total_shares'])
            stock['p_and_l'] = (stock['current_price'] - stock['average_price']) * Decimal(stock['total_shares'])

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

def transactions_list(request, id):
    portfolio = get_object_or_404(Portfolio, pk=id)
    transactions = StockTransaction.objects.filter(portfolio=portfolio)
    context = {
        'portfolio': portfolio,
        'transactions': transactions
    }
    return render(request, 'portfolio/transactions_list.html', context)