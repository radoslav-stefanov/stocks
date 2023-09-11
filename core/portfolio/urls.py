from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create-portfolio', views.create_portfolio, name='create-portfolio'),
    path('portfolio/<id>/', views.portfolio_detail, name='portfolio-detail'),
    path('portfolio/<int:portfolio_id>/add_stock_transaction/', views.add_stock_transaction, name='add-stock-transaction'),
    path('portfolio/<int:portfolio_id>/edit_stock_transaction/<int:id>/', views.edit_stock_transaction, name='edit-stock-transaction'),
    path('portfolio/<int:portfolio_id>/delete_stock_transaction/<int:id>/', views.delete_stock_transaction, name='delete-stock-transaction'),
    path('edit-portfolio/<int:id>/', views.edit_portfolio, name='edit-portfolio'),
    path('delete-portfolio/<int:id>/', views.delete_portfolio, name='delete-portfolio'),
    path('portfolio/<int:portfolio_id>/delete-transaction/<int:id>/', views.delete_transaction, name='delete-transaction'),
    path('portfolio/<id>/transactions/', views.transactions_list, name='transactions-list'),
]
