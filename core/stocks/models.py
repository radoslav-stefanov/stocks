from django.db import models
from authentication.models import User
from helpers.models import TrackingModel

# Create your models here.

class Transaction(TrackingModel):
    stock_name = models.CharField(max_length=100)
    stock_price = models.FloatField()
    #owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.stock_name