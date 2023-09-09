from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add-transaction', views.add_transaction, name='add-transaction'),
]