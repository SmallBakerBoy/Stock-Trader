from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

# Create your views here.
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())

def assets(request):
    template = loader.get_template('assets.html')
    return HttpResponse(template.render())

def watchlist(request):
    template = loader.get_template('watchlist.html')
    return HttpResponse(template.render())

def account(request):
    template = loader.get_template('account.html')
    return HttpResponse(template.render())

def sign_up(request):
    if request.method == 'POST':
        form = CreateAccount(request.POST)
    else:
        form = CreateAccount()
    return render(request,'registration/sign_up.html',{'form':form})