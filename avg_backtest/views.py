from django.shortcuts import render, redirect
from investment.models import StockData
from .forms import AvgBacktestForm
from django.http import HttpResponse
import pandas as pd
from tools.grapic import generate_cost_revenue_image, generate_price_movement_image
from tools.data import get_data_from_db

def backtest(request):
    return render(request, 'backtest.html')

def avg_backtest(request):
    return render(request, 'investment/backtest/avg_backtest_page.html')

def cal_avg_return(ticker, amount, buy_condition_parms, sell_condition_parms, start_date = None, end_date = None):
    data = get_data_from_db(ticker, start_date, end_date)
    monthly_amount = amount
    data['shares'] = 0
    data['rest_money'] = 0
    data['cumulative_cost'] = 0
    shares = 0
    rest_money = 0
    prev = 0
    cost = 0
    for i in range(len(data)):
        if data.iloc[i]['Day'] > buy_condition_parms:
            today = 1
        elif data.iloc[i]['Day'] == buy_condition_parms:
            today = 0
        else:
            today = -1
        if today == 0 or today - prev == 2:
            rest_money += monthly_amount
            cost += monthly_amount
            close = round(data.iloc[i]['Close'],2)
            buy_share = rest_money // close
            shares += buy_share
            rest_money = rest_money - buy_share * close
        prev = today
        data.loc[i, 'shares'] = shares
        data.loc[i, 'rest_money'] = rest_money
        data.loc[i, 'cumulative_cost'] = cost
    # summation
    data['shares_diff'] = data['shares'].diff()
    data['amount'] = data['Close'] * data['shares'] + data['rest_money']
    return data

def avg_backtest_result(request):
    if request.method == 'POST':
        strategy_type = 'Dollar Cost Averaging'
        ticker = request.POST['ticker']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if start_date > end_date:
            return HttpResponse('Start date cannot be greater than end date.')
        amount = float(request.POST['amount'])
        buy_condition_parms = int(request.POST['days'])
        sell_condition_parms = None
        return_data = cal_avg_return(ticker, amount, buy_condition_parms, sell_condition_parms, start_date, end_date)
        buy_condition = 'Buy on day {} every month'.format(buy_condition_parms)
        sell_condition = 'None'
        total_cost = return_data['cumulative_cost'].iloc[-1]
        total_revenue = return_data['amount'].iloc[-1]
        price_movement_image = generate_price_movement_image(return_data)
        cost_revenue_image = generate_cost_revenue_image(return_data)
        return render(request, 'investment/backtest/backtest_results.html', {'ticker': ticker, 'strategy_type': strategy_type,
                'start_date': start_date, 'end_date': end_date,
                'buy_condition': buy_condition, 'sell_condition': sell_condition,
                'initial_money' : amount, 'total_cost': total_cost, 'total_revenue': total_revenue,
                'price_movement_image': price_movement_image, 'cost_revenue_image': cost_revenue_image})
    else:
        form = AvgBacktestForm()
    return render(request, 'investment/backtest/avg_backtest_page.html', {'form': form})