from django import forms
from .models import blacklist,user_settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateAccount(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email']

    def clean_username(self):
        username = self.cleaned_data['username']

        if len(username)<7 or len(username)>17:
            raise forms.ValidationError('The username is not valid, it must be between 8 and 16 alphanumeric characters')
        return username


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
        return ticker.upper()
    
class UpdateRisk(forms.ModelForm):
    class Meta:
        model = user_settings
        fields = ['risk_level','ideal']
    
