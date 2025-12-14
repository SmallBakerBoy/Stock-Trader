from django import forms
from .models import blacklist
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateAccount(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email']

class BlacklistCompany(forms.ModelForm):
    ticker = forms.CharField(max_length=5)

    class Meta:
        model = blacklist
        fields = ['ticker']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_ticker(self):
        ticker = self.cleaned_data['ticker']

        if blacklist.objects.filter(user=self.user, ticker=ticker).exists():
            raise forms.ValidationError("You already added this ticker.")






'''class user(models.Model):
    UserID = models.AutoField(auto_created=True, primary_key=True, verbose_name='UID')
    Username = models.CharField(max_length=32)
    Password = models.CharField(max_length=128)
   
    Email = models.EmailField()
    Phone = models.CharField(max_length=15)
   
    Balance = models.FloatField(default=1000.0)
    Profit = models.FloatField(default = 0.0)'''
