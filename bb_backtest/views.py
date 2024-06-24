from django.shortcuts import render, redirect
from investment.models import StockData
import pandas as pd
from tools.grapic import generate_cost_revenue_image, generate_price_movement_image
from tools.data import get_data_from_db, get_data_from_db_before_date
from .forms import BbBacktestForm
from django.http import HttpResponse

def backtest(request):
    return render(request, 'backtest.html')

def bb_backtest(request):
    return render(request, 'investment/backtest/bb_backtest_page.html')

def cal_bb_return(ticker, init, ma, buy_condition_parm, sell_condition_parm, start_date = None, end_date = None):
    # get previous ma data before start_date
    previous_data = get_data_from_db_before_date(ticker, start_date, ma)
    data = get_data_from_db(ticker, start_date, end_date)

    # concat data
    data = pd.concat([previous_data, data], axis=0)
    data.sort_values(by='Date', inplace=True)
    data = data.reset_index()

    # prepare data
    data['MA'] = data['Close'].rolling(window=ma).mean().shift(1)
    data['std'] = data['Close'].rolling(window=ma).std().shift(1)
    data['upper_band'] = data['MA'] + (data['std'] * buy_condition_parm[1])
    data['lower_band'] = data['MA'] - (data['std'] * buy_condition_parm[1])
    data['cumulative_cost'] = init
    data['shares'] = 0
    data['signal'] = 0
    data['rest_money'] = 0
    data.loc[(data['MA'] >= 0) & (data['Close'] > data['upper_band']), 'signal'] = 1
    data.loc[(data['MA'] >= 0) & (data['Close'] < data['lower_band']), 'signal'] = -1
    data.dropna()
    # calculate return
    rest_money = init
    shares = 0
    for i in range(len(data)):
        if data.iloc[i]['signal'] == 1 and shares == 0:
            close = round(data.iloc[i]['Close'],2)
            shares = rest_money // close
            rest_money = rest_money - shares * close
        elif data.iloc[i]['signal'] == -1 and shares > 0:
            close = round(data.iloc[i]['Close'],2)
            rest_money = rest_money + shares * close
            shares = 0
        data.loc[i, 'shares'] = shares
        data.loc[i, 'rest_money'] = rest_money

    # summation
    data['shares_diff'] = data['shares'].diff()
    data['amount'] = data['Close'] * data['shares'] + data['rest_money']
    return data

def bb_backtest_result(request):
    if request.method == 'POST':
        # form = BbBacktestForm(request.POST)
        # if form.is_valid():
        strategy_type = 'Bollinger Band'
        ticker = request.POST['ticker']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        if start_date > end_date:
            return HttpResponse('Start date cannot be greater than end date.')
        init = int(request.POST['initial_money'])
        ma = int(request.POST['ma'])
        std = int(request.POST['std'])
        buy_condition_parm = [ma, std]
        sell_condition_parm = [ma, std]
        buy_condition = 'if close price larger than {}ma + {} x std'.format(buy_condition_parm[0], buy_condition_parm[1])
        sell_condition = 'if close price smaller than {}ma - {} x std'.format(sell_condition_parm[0], sell_condition_parm[1])
        return_data = cal_bb_return(ticker, init, ma, buy_condition_parm, sell_condition_parm, start_date, end_date)
        total_cost = return_data['cumulative_cost'].iloc[-1]
        total_revenue = round(return_data['amount'].iloc[-1] - init,2)
        price_movement_image = generate_price_movement_image(return_data)
        cost_revenue_image = generate_cost_revenue_image(return_data)
        return render(request, 'investment/backtest/backtest_results.html', {'ticker': ticker, 'strategy_type': strategy_type,
                'start_date': start_date, 'end_date': end_date,
                'buy_condition': buy_condition, 'sell_condition': sell_condition,
                'initial_money' : init, 'total_cost': total_cost, 'total_revenue': total_revenue,
                'price_movement_image': price_movement_image, 'cost_revenue_image': cost_revenue_image})
        # else:
        #     print(form.errors)
    else:
        form = BbBacktestForm()
    return render(request, 'investment/backtest/bb_backtest_page.html', {'form': form})