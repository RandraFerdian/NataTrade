from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone

class TradeLog(models.Model):
    # Pilihan Strategi (Automated based on duration)
    STRATEGY_CHOICES = [
        ('SCALPING', 'Scalping'),
        ('INTRADAY', 'Intraday Trading'),
        ('SWING', 'Swing Trading'),
        ('POSITION', 'Position Trading'),
    ]
    
    # Opsi Posisi Trade
    SIDE_CHOICES = [
        ('LONG', 'Long Position'),
        ('SHORT', 'Short Position'),
    ]
    
    # Status hasil trading
    STATUS_CHOICES = [
        ('WIN', 'Profit'),
        ('LOSS', 'Loss'),
        ('BE', 'Break Even'),
    ]

    # Relasi User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Detail Transaksi
    asset_pair = models.CharField(max_length=20, help_text="Contoh: BTC/USDT")
    side = models.CharField(max_length=5, choices=SIDE_CHOICES, default='LONG')
    strategy_type = models.CharField(max_length=20, choices=STRATEGY_CHOICES, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='BE')
    
    # Variabel Waktu
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(default=timezone.now)
    
    # Variabel Harga & Size
    entry_price = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0000'))
    exit_price = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0000'))
    position_size_usdt = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.0000'), help_text="Margin yang digunakan")
    leverage = models.IntegerField(default=1)
    quantity = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.0000'), blank=True)
    
    # Variabel PNL & Fee (Dihitung Otomatis)
    gross_pnl = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.0000'), blank=True) 
    entry_fee = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.0000'))
    exit_fee = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.0000'))
    funding_fee = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.0000'))
    gas_fee = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.0000'))
    
    # Risk Management & Analisa
    risk_amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.0000'))
    planned_rr = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.0000'))
    tags = models.CharField(max_length=100, blank=True, help_text="Contoh: #FOMO #Plan")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 1. HITUNG QUANTITY & TOTAL POSITION SIZE
        total_position_size = self.position_size_usdt * Decimal(self.leverage)
        
        if self.entry_price > 0:
            self.quantity = total_position_size / self.entry_price

        # 2. HITUNG ESTIMASI FEE OTOMATIS (Jika diisi 0, asumsi 0.05% per side)
        fee_rate = Decimal('0.0005') 
        if self.entry_fee == 0:
            self.entry_fee = total_position_size * fee_rate
        if self.exit_fee == 0:
            self.exit_fee = total_position_size * fee_rate

        # 3. HITUNG GROSS P&L (Berdasarkan Side Long/Short)
        if self.entry_price > 0 and self.exit_price > 0 and self.quantity > 0:
            if self.side == 'LONG':
                self.gross_pnl = (self.exit_price - self.entry_price) * self.quantity
            else: # SHORT
                self.gross_pnl = (self.entry_price - self.exit_price) * self.quantity

        # 4. TENTUKAN STATUS OTOMATIS BERDASARKAN NET P&L
        # Kita panggil total_fees di sini untuk cek status akhir
        net_result = self.gross_pnl - (self.entry_fee + self.exit_fee + self.funding_fee + self.gas_fee)
        
        if net_result > 0:
            self.status = 'WIN'
        elif net_result < 0:
            self.status = 'LOSS'
        else:
            self.status = 'BE'

        # 5. OTOMASI STRATEGY TYPE BERDASARKAN DURASI HOLD
        duration = self.exit_time - self.entry_time
        hours = duration.total_seconds() / 3600
        days = duration.days

        if hours < 1:
            self.strategy_type = 'SCALPING'
        elif hours < 24:
            self.strategy_type = 'INTRADAY'
        elif days < 14:
            self.strategy_type = 'SWING'
        else:
            self.strategy_type = 'POSITION'

        super(TradeLog, self).save(*args, **kwargs)

    @property
    def total_fees(self):
        """Total akumulasi semua biaya"""
        return self.entry_fee + self.exit_fee + self.funding_fee + self.gas_fee

    @property
    def net_pnl(self):
        """Hasil bersih setelah dikurangi biaya"""
        return self.gross_pnl - self.total_fees

    @property
    def hold_duration(self):
        """Durasi menahan posisi"""
        return self.exit_time - self.entry_time

    def __str__(self):
        return f"{self.user.username} | {self.asset_pair} | {self.status}"

class TradingAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    initial_balance = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Account {self.user.username}"