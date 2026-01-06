from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TradeLog, TradingAccount 
from .form import TradeLogForm
from django.db.models import Sum
from decimal import Decimal

@login_required
def nata_strategi_view(request):
    """
    View untuk mengelola jurnal strategi, input transaksi, 
    dan pemantauan saldo akun trading.
    """
    
    # --- SECTION 1: MANAJEMEN AKUN & MODAL ---
    # Mendapatkan atau membuat akun trading untuk user yang login
    account, created = TradingAccount.objects.get_or_create(user=request.user)
    
    # Logika untuk update Modal Awal (Initial Balance)
    if request.method == 'POST' and 'update_modal' in request.POST:
        new_balance = request.POST.get('initial_balance')
        if new_balance:
            account.initial_balance = Decimal(new_balance)
            account.save()
        return redirect('nata_strategi')
    
    # --- SECTION 2: INPUT TRANSAKSI (TRADELOG) ---
    if request.method == 'POST' and 'update_modal' not in request.POST:
        form = TradeLogForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user = request.user
            trade.save()
            return redirect('nata_strategi')
    else:
        form = TradeLogForm()

    # --- SECTION 3: PENGOLAHAN DATA & ANALITIK ---
    # Mengambil semua riwayat transaksi user
    trades = TradeLog.objects.filter(user=request.user).order_by('-exit_time')
    total_trades = trades.count()
    
    # Perhitungan Keuangan (Audit Logic)
    initial_capital = account.initial_balance
    
    # Menghitung Total Gross P&L
    total_gross_pnl = trades.aggregate(total=Sum('gross_pnl'))['total'] or Decimal('0.00')
    
    # Menghitung Total Biaya (Fees)
    # Catatan: Pastikan model TradeLog memiliki properti/method 'total_fees'
    total_fees = sum(trade.total_fees for trade in trades)
    
    # Menghitung Net P&L dan Saldo Berjalan (Current Balance)
    net_pnl = total_gross_pnl - total_fees
    current_balance = initial_capital + net_pnl
    
    # Statistik Performa (Win Rate & Profit Factor)
    win_count = trades.filter(status='WIN').count()
    win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0
    
    gross_profit = trades.filter(status='WIN').aggregate(total=Sum('gross_pnl'))['total'] or Decimal('0.00')
    gross_loss = trades.filter(status='LOSS').aggregate(total=Sum('gross_pnl'))['total'] or Decimal('0.00')
    
    # Menghitung Profit Factor (Gross Profit / Absolute Gross Loss)
    if gross_loss != 0:
        profit_factor = abs(gross_profit) / abs(gross_loss)
    else:
        profit_factor = 0

    # --- SECTION 4: PENGIRIMAN DATA KE TEMPLATE ---
    context = {
        'form': form,
        'trades': trades,
        'modal_awal': initial_capital,
        'saldo_saiki': current_balance,
        'total_net_pnl': net_pnl,
        'win_rate': round(win_rate, 2),
        'profit_factor': round(profit_factor, 2),
        'total_trades': total_trades,
    }
    
    return render(request, 'strategy/nata_strategi.html', context)

@login_required
def edit_trade_view(request, pk):
    trade = get_object_or_404(TradeLog, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TradeLogForm(request.POST, instance=trade)
        if form.is_valid():
            form.save() # Otomatis hitung ulang P&L di model
            return redirect('nata_strategi')
    return redirect('nata_strategi')