from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create-portfolio', views.create_portfolio, name='create-portfolio'),
    path('portfolio/<id>/', views.portfolio_detail, name='portfolio-detail'),
    path('portfolio/<portfolio_id>/add_stock_transaction/', views.add_stock_transaction, name='add-stock-transaction'),
]
