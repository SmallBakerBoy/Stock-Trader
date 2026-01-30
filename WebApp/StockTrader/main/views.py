from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .forms import CreateAccount,BlacklistCompany
from .models import blacklist,assets,watchlist_items,trades
from .Trading_Algorithm.main import queue

# Create your views here.
@login_required(login_url='/login')
def home(request):
    user_assets = assets.objects.filter(user = request.user)
    user_trades = trades.objects.filter(user = request.user)        
    return render(request, 'home.html',{'assets':user_assets,'trades':user_trades})

@csrf_protect
@login_required(login_url='/login')
def create_portfolio(request):
    if request.method=='POST':
        settings = request.body
        queue(settings)
    return redirect('/home')

def landing(request):
    template = loader.get_template('landing.html')
    return HttpResponse(template.render())

@login_required(login_url='/login')
def asset(request):
    user_asset = assets.objects.filter(user = request.user)                                                                                                                               
    return render(request, 'assets.html',{'assets':user_asset})


@login_required(login_url='/login')
def watchlists(request):
    watchlist_list = watchlist_items.objects.filter(user = request.user)
    user_watchlists = ((watchlist_list.values_list('watchlist',flat=True)).distinct())
    return render(request, 'watchlist.html',{'watchlists':user_watchlists,'watchlist_items':watchlist_list})

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

