# avg_backtest/forms.py

from django import forms
from investment.models import StockData
from django.core.exceptions import ValidationError

class AvgBacktestForm(forms.Form):
    ticker = forms.ModelChoiceField(queryset=StockData.objects.values_list('Ticker', flat=True).distinct(), required=True)
    # ticker = forms.CharField(label='Ticker', max_length=10)
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    amount = forms.IntegerField(label='Amount', min_value=1)
    days = forms.IntegerField(label='Days', min_value=1, max_value=31)