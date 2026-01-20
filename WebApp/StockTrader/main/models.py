from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user_settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    risk_level = models.IntegerField()
    ideal = models.BooleanField()

class watchlist_items(models.Model):
    ticker = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist = models.IntegerField()

class blacklist(models.Model):
    ticker = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'ticker')

class trades(models.Model):
    tradeID = models.AutoField(auto_created=True, primary_key=True, verbose_name='TID')
    ticker = models.CharField(max_length=5)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    type = models.BooleanField()
    amount = models.FloatField()

    buyPrice = models.FloatField()
    sellPrice = models.FloatField()
    profit = models.FloatField()


class assets(models.Model):
    ticker = models.CharField(max_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.FloatField()
    price = models.FloatField()
