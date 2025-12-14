from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .forms import CreateAccount,BlacklistCompany
from .models import blacklist

# Create your views here.
@login_required(login_url='/login')
def home(request):
    return render(request, 'home.html')

def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())

@login_required(login_url='/login')
def assets(request):
    return render(request, 'assets.html')

@login_required(login_url='/login')
def watchlist(request):
    return render(request, 'watchlist.html')

@login_required(login_url='/login')
def account(request):
    blacklisted = blacklist.objects.filter(user = request.user)
    if request.method == 'POST':
        form = BlacklistCompany(request.POST, user = request.user)
        if form.is_valid():
            new_blacklist = form.save(commit=False)
            new_blacklist.user = request.user
            new_blacklist.save()
            return redirect('/account')
    else:
        form = BlacklistCompany(user = request.user)

    return render(request, 'account.html',{'form':form, 'blacklisted':blacklisted})

def signup(request):
    if request.method == 'POST':
        form = CreateAccount(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/home')
    else:
        form = CreateAccount()
    return render(request,'registration/signup.html',{'form':form})