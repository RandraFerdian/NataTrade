from django import forms
from .models import TradeLog

class TradeLogForm(forms.ModelForm):
    class Meta:
        model = TradeLog
        # 1. Pilih field sing bakal diisi manual dening user
        fields = [
            'asset_pair', 'side', 'status', 'entry_time', 'exit_time',
            'entry_price', 'exit_price', 'position_size_usdt', 'quantity',
            'leverage', 'gross_pnl', 'entry_fee', 'exit_fee', 
            'funding_fee', 'gas_fee', 'risk_amount', 'planned_rr', 
            'tags', 'notes'
        ]
        
        # 2. Widgets: Ngerubah tampilan standar dadi luwih canggih
        widgets = {
            'entry_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'exit_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Piye analisamu mau?'}),
            'asset_pair': forms.TextInput(attrs={'placeholder': 'BTC/USDT'}),
        }

    # 3. Styling Otomatis nganggo Tailwind CSS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'w-full bg-white/50 border border-slate-200 rounded-xl px-4 py-3 '
                    'text-sm focus:ring-2 focus:ring-indigo-500 outline-none transition-all'
                )
            })