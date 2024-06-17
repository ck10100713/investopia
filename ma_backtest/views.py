from django.shortcuts import render

# Create your views here.
def ma_backtest(request):
    return render(request, 'investment/backtest/ma_backtest_page.html')