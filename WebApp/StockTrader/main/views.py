from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .forms import CreateAccount,BlacklistCompany
from .models import blacklist,assets,watchlist_items,trades
from .Trading_Algorithm.main import queue
from .Trading_Algorithm.market_data import get_company_info,api_search
from .Trading_Algorithm.database import update_asset


# Create your views here.
@login_required(login_url='/login')
def home(request):
    user_assets = assets.objects.filter(user = request.user)
    watchlist_list = watchlist_items.objects.filter(user = request.user)
    user_watchlists = ((watchlist_list.values_list('watchlist',flat=True)).distinct())
    blacklisted = blacklist.objects.filter(user = request.user)
    user_trades = trades.objects.filter(user = request.user)        
    return render(request, 'home.html',{'watchlists':user_watchlists,'assets':user_assets,'trades':user_trades,'blacklisted':blacklisted})

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

def update(request):
    if request.method == 'POST':
        msg,code = update_asset(request.body)
        if code == 200:
            return JsonResponse({'success':True})
        else:
            return JsonResponse(msg,status=code)

def company(request):
    if request.method == 'POST':
        company_data = get_company_info(request.body)
        return JsonResponse(company_data,safe=False)

def search(request):
    if request.method == 'POST':
        results = api_search(request.body)
        return JsonResponse(results, safe=False)

@login_required(login_url='/login')
def account(request):
    form = BlacklistCompany(user = request.user)
    blacklisted = blacklist.objects.filter(user = request.user)
    if request.method == 'POST':
        if 'Blacklist' in request.POST:
            form = BlacklistCompany(request.POST, user = request.user)
            if form.is_valid():
                new_blacklist = form.save(commit=False)
                new_blacklist.user = request.user
                new_blacklist.save()
                return redirect('/account')
        elif 'AccountInfo' in request.POST:
            if request.POST.get('ideal') != 'on':
                request.user.risk_level = request.POST.get('risk_level')
            else:
                request.user.risk_level = -1
            request.user.save()
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

