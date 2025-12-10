from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('assets/', views.assets, name='assets'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('account/', views.account, name='account'),
    path('signup/', views.signup, name='signup'),
]