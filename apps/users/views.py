from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from apps.asset.models import InvestementLog
from apps.mental.models import MentalAudit
from apps.strategy.models import TradeLog

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registrasi berhasil!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard_view(request):
    # 1. Hitung Profit Trading (Nata Strategi)
    trades = TradeLog.objects.filter(user=request.user)
    trading_profit = sum(t.net_pnl for t in trades) # Menggunakan @property net_pnl

    # 2. Hitung Profit Investasi (Nata Aset)
    investments = InvestementLog.objects.filter(user=request.user)
    investment_profit = investments.aggregate(Sum('total_profit'))['total_profit__sum'] or 0

    # 3. Gabungkan Total Profit
    total_combined_profit = trading_profit + investment_profit

    # 4. Ambil Skor Mental Terakhir (Nata Mental)
    last_audit = MentalAudit.objects.filter(user=request.user).last()
    final_mental_score = last_audit.combined_score if last_audit else 0
    
    context = {
        'total_pnl': total_combined_profit,
        'trading_pnl': trading_profit,
        'invest_pnl': investment_profit,
        'mental_score': final_mental_score,
        'recent_trades': trades.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html')


def logout_view(request):
    return redirect('landing')