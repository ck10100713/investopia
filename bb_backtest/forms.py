# bb_backtest/forms.py

from django import forms
from investment.models import StockData

class BbBacktestForm(forms.Form):
    ticker = forms.ModelChoiceField(queryset=StockData.objects.values_list('Ticker', flat=True).distinct(), required=True)
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    initial_money = forms.IntegerField(label='initial_money', min_value=1)
    ma = forms.IntegerField(label='ma', min_value=1, max_value=99)
    std = forms.IntegerField(label='standard deviation', min_value=1, max_value=3)