from django.db import models

# Create your models here.
class user(models.Model):
    UserID = models.AutoField(auto_created=True, primary_key=True, verbose_name='UID')
    Username = models.CharField(max_length=32)
    Password = models.CharField(max_length=128)
   
    Email = models.EmailField()
    Phone = models.CharField(max_length=15)
   
    Balance = models.FloatField(default=1000.0)
    Profit = models.FloatField(default = 0.0)

class watchlist(models.Model):
    Ticker = models.CharField(max_length=5)
    User = models.IntegerField()
    Watchlist = models.IntegerField()

class blacklist(models.Model):
    Ticker = models.CharField(max_length=5)
    User = models.IntegerField()

class trades(models.Model):
    TradeID = models.AutoField(auto_created=True, primary_key=True, verbose_name='TID')
    Ticker = models.CharField(max_length=5)

    Type = models.BooleanField()
    Amount = models.FloatField()

    BuyPrice = models.FloatField()
    SellPrice = models.FloatField()
    Profit = models.FloatField()


class assets(models.Model):
    Ticker = models.CharField(max_length=5)
    User = models.IntegerField()

    Amount = models.FloatField()
    Price = models.FloatField()
