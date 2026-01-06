from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TradeLog, TradingAccount 
from .form import TradeLogForm
from django.db.models import Sum
from decimal import Decimal
from django.utils import timezone
from datetime import datetime
import calendar

@login_required
def nata_strategi_view(request):
    account, created = TradingAccount.objects.get_or_create(user=request.user)
    
    # --- 1. LOGIKA NAVIGASI TANGGAL ---
    now = timezone.now()
    # Njupuk sasi lan tahun seko URL, nek ora ana nganggo sasi saiki
    selected_month = int(request.GET.get('month', now.month))
    selected_year = int(request.GET.get('year', now.year))

    # Navigasi prev/next sasi
    prev_month = selected_month - 1 if selected_month > 1 else 12
    prev_year = selected_year if selected_month > 1 else selected_year - 1
    next_month = selected_month + 1 if selected_month < 12 else 1
    next_year = selected_year if selected_month < 12 else selected_year + 1

    # Ngitung pira dinane neng sasi kuwi
    _, num_days = calendar.monthrange(selected_year, selected_month)
    days_range = range(1, num_days + 1)
    
    month_names = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                   "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

    # --- 2. LOGIKA INPUT DATA ---
    if request.method == 'POST':
        if 'update_modal' in request.POST:
            new_balance = request.POST.get('initial_balance')
            if new_balance:
                account.initial_balance = Decimal(new_balance)
                account.save()
            return redirect('nata_strategi')
        
        form = TradeLogForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.user = request.user
            trade.save()
            return redirect('nata_strategi')
    else:
        form = TradeLogForm()

    # --- 3. FILTER DATA (Kunci Perbaikan) ---
    all_user_trades = TradeLog.objects.filter(user=request.user)
    
    # Filter trades khusus kanggo sasi lan tahun sing dipilih
    filtered_trades = all_user_trades.filter(
        exit_time__month=selected_month, 
        exit_time__year=selected_year
    ).order_by('-exit_time')

    # --- 4. LOGIKA HEATMAP (Ngango data filtered) ---
    heatmap_data = {}
    for trade in filtered_trades:
        day = trade.exit_time.day
        val = float(trade.net_pnl) # net_pnl seko property neng models
        heatmap_data[day] = heatmap_data.get(day, 0) + val

    # --- 5. ITUNG-ITUNGAN STATISTIK ---
    # Saldo Saiki tetep global (kabeh trade) supaya akurat karo dompet
    total_gross_pnl = all_user_trades.aggregate(total=Sum('gross_pnl'))['total'] or Decimal('0.00')
    total_fees = sum(t.total_fees for t in all_user_trades)
    saldo_saiki = account.initial_balance + total_gross_pnl - total_fees

    # Statistik Bulanan (nggo kothak/card neng ndhuwur)
    total_month_net_pnl = sum(t.net_pnl for t in filtered_trades)
    win_count = filtered_trades.filter(status='WIN').count()
    total_month_trades = filtered_trades.count()
    month_win_rate = (win_count / total_month_trades * 100) if total_month_trades > 0 else 0

    context = {
        'form': form,
        'trades': filtered_trades, # Tabel saiki mung isi data sasi sing dipilih
        'heatmap_data': heatmap_data,
        'days_range': days_range,
        'month_name': month_names[selected_month],
        'curr_year': selected_year,
        'prev_m': prev_month, 'prev_y': prev_year,
        'next_m': next_month, 'next_y': next_year,
        'modal_awal': account.initial_balance,
        'saldo_saiki': saldo_saiki,
        'total_net_pnl': total_month_net_pnl, # Bathi/rugi sasi iki wae
        'win_rate': round(month_win_rate, 2),
        'total_trades': total_month_trades,
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