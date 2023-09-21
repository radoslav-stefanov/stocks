from django.db import models
from authentication.models import User
from helpers.models import TrackingModel

class Portfolio(TrackingModel):
    portfolio_name = models.CharField(max_length=100)
    portfolio_description = models.TextField()

    def __str__(self):
        return self.portfolio_name

class StockTransaction(TrackingModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    shares = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ticker} - {self.date}"

class DataSpy(models.Model):
    date = models.DateField(primary_key=True)
    adjusted_close_price = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        db_table = 'data_spy'