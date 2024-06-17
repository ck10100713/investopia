from django.shortcuts import render

# Create your views here.
def bb_backtest(request):
    return render(request, 'investment/backtest/bb_backtest_page.html')