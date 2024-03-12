# users/views.py
from .forms import ProfileUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import Wallet, Transaction, Event
from .forms import WalletTopUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})
    

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def wallet_topup(request):
    if request.method == 'POST':
        form = WalletTopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.wallet_balance += amount
            request.user.save()
            return redirect('topup_success')
    else:
        form = WalletTopUpForm()
    return render(request, 'top_up.html', {'form': form})

def topup_success(request):
    return render(request, 'users/topup_success.html')

@login_required
def withdraw_earnings(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        wallet = Wallet.objects.get(user=request.user)
        if wallet.balance >= amount:
            wallet.balance -= amount
            wallet.save()
            Transaction.objects.create(user=request.user, amount=amount, transaction_type='Withdrawal')
            return redirect('wallet')
        else:
            return render(request, 'insufficient.html')
    return render(request, 'withdraw.html')

@login_required
def user_profile(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user, balance=0)

    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'user_profile.html', {'wallet': wallet, 'transactions': transactions})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})