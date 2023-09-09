from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create-portfolio', views.create_portfolio, name='create-portfolio'),
]
