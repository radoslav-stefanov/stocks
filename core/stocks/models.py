from django.db import models
from authentication.models import User
from helpers.models import TrackingModel

# Create your models here.

class Stocks(TrackingModel):
    portfolio_name = models.CharField(max_length=100)
    portfolio_description = models.TextField()
    #owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.portfolio_name
