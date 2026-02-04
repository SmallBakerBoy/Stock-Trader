from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    balance = models.DecimalField(default=10000.00,max_digits=12,decimal_places=2)
    risk_level = models.IntegerField(default=50)

class watchlist_items(models.Model):
    ticker = models.CharField(max_length=5)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    watchlist = models.IntegerField()

class blacklist(models.Model):
    ticker = models.CharField(max_length=5)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'ticker')

class trades(models.Model):
    tradeID = models.AutoField(auto_created=True, primary_key=True, verbose_name='TID')
    ticker = models.CharField(max_length=5)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    type = models.BooleanField()
    amount = models.DecimalField(max_digits=12,decimal_places=2)


class assets(models.Model):
    ticker = models.CharField(max_length=5)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=12,decimal_places=2)
    price = models.DecimalField(max_digits=12,decimal_places=2)
