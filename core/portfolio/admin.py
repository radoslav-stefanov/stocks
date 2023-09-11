from django.contrib import admin

from .models import Portfolio, StockTransaction

admin.site.register(Portfolio)
admin.site.register(StockTransaction)