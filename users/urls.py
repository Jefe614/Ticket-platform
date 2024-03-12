from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('top-up/', views.wallet_topup, name='top_up_wallet'),
    path('withdraw-earnings/', views.withdraw_earnings, name='withdraw_earnings'),
    path('top-up/success/', views.topup_success, name='top_up_success'),
    path('profile/', views.user_profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile')
]