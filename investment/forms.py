from django import forms
from django.utils.translation import gettext_lazy as _ # 新增
from .models import StockData

class InvestmentForm(forms.Form):
    name = forms.CharField(label=_('Name'), max_length=100)
    amount = forms.FloatField(label=_('Amount'))
    interest_rate = forms.FloatField(label=_('Interest Rate'))
    duration = forms.IntegerField(label=_('Duration'))
    result = forms.FloatField(label=_('Result'), required=False)
    created_at = forms.DateTimeField(label=_('Created At'), required=False)
    updated_at = forms.DateTimeField(label=_('Updated At'), required=False)

    def calculate(self):
        self.result = self.amount * (1 + self.interest_rate / 100 * self.duration)
        return self.result
    def __str__(self):
        return self.result

class ReturnCalculatorForm(forms.Form):
    amount = forms.DecimalField(label="Investment Amount", max_digits=12, decimal_places=2)
    months = forms.IntegerField(label="Number of Months")
    rate = forms.DecimalField(label="Expected Return Rate (%)", max_digits=5, decimal_places=2)

# class StrategyForm(forms.Form):
#     strategy = forms.ChoiceField()

class StragetyForm(forms.Form):
    ticker = forms.ChoiceField(
        choices=[(ticker, ticker) for ticker in StockData.objects.values_list('Ticker', flat=True).distinct()],
        required=True,
        label="Stock List"
    )
    # for avg
    days = forms.IntegerField(min_value=1, max_value=30, required=False)
    amount = forms.IntegerField(min_value=1, required=False)
    # for avg

    # for bb
    std_dev = forms.IntegerField(min_value=1, required=False)
    # for bb
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    def clean(self):
        cleaned_data = super().clean()
        backtest_type = self.data.get('backtest_type')
        if backtest_type == 'avg':
            if not cleaned_data.get('days') or not cleaned_data.get('amount'):
                raise forms.ValidationError('Days 和 Amount 是必須的')
        return cleaned_data