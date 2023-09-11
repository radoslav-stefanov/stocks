from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockTransaction
from django.core.cache import cache

@receiver(post_save, sender=StockTransaction)
def clear_portfolio_cache(sender, **kwargs):
    portfolio_id = kwargs['instance'].portfolio.id
    cache_key = f'portfolio_{portfolio_id}_summary'
    cache.delete(cache_key)
