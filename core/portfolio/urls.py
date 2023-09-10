from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create-portfolio', views.create_portfolio, name='create-portfolio'),
    path('portfolio/<id>/', views.portfolio_detail, name='portfolio-detail'),
    path('portfolio/<int:portfolio_id>/add_stock_transaction/', views.add_stock_transaction, name='add-stock-transaction'),
    path('portfolio/<int:portfolio_id>/edit_stock_transaction/<int:id>/', views.edit_stock_transaction, name='edit-stock-transaction'),
    path('portfolio/<int:portfolio_id>/delete_stock_transaction/<int:id>/', views.delete_stock_transaction, name='delete-stock-transaction'),
]
