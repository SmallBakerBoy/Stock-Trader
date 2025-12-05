from django.db import models

# Create your models here.
class User(models.Model):
    UserID = models.BigAutoField(auto_created=True, primary_key=True)
    Username = models.CharField(max_length=32)
    '''Password

    Email
    Phone

    Balance
    Profit'''