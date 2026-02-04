from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('home/create', views.create_portfolio, name='create_portfolio'),
    path('assets/', views.asset, name='assets'),
    path('watchlist/', views.watchlists, name='watchlist'),
    path('search/', views.search, name='search'),
    path('company/', views.company, name='company'),
    path('account/', views.account, name='account'),
    path('signup/', views.signup, name='signup'),
]