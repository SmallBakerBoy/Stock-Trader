from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('assets/', views.asset, name='assets'),
    path('watchlist/', views.watchlists, name='watchlist'),
    path('account/', views.account, name='account'),
    path('signup/', views.signup, name='signup'),
]