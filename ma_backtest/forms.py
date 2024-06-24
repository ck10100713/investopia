# bb_backtest/forms.py

from django import forms
from investment.models import StockData

class BbBacktestForm(forms.Form):
    ticker = forms.ModelChoiceField(queryset=StockData.objects.values_list('Ticker', flat=True).distinct(), required=True)
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    initial_money = forms.IntegerField(label='initial_money', min_value=1)
    short_ma = forms.IntegerField(label='short_ma', min_value=1)
    mid_ma = forms.IntegerField(label='mid_ma', min_value=1)
    long_ma = forms.IntegerField(label='long_ma', min_value=1)