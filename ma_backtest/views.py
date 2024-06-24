from django.shortcuts import render, redirect
from investment.models import StockData
import pandas as pd
from tools.grapic import generate_cost_revenue_image, generate_price_movement_image
from tools.data import get_data_from_db, get_data_from_db_before_date

# Create your views here.
def ma_backtest(request):
    return render(request, 'investment/backtest/ma_backtest_page.html')

def backtest(request):
    return render(request, 'backtest.html')

def cal_ma_return(ticker, init, buy_condition_parms, sell_condition_parms, start_date = None, end_date = None):
    short = min(buy_condition_parms)
    long = max(buy_condition_parms)
    mid = sum(buy_condition_parms) - short - long

    # get previous ma data before start_date
    previous_data = get_data_from_db_before_date(ticker, start_date, short)
    data = get_data_from_db(ticker, start_date, end_date)
    # concat data
    data = pd.concat([previous_data, data], axis=0)
    data.sort_values(by='Date', inplace=True)
    data = data.reset_index()
    # prepare data
    data['short_MA'] = data['Close'].rolling(window=short).mean().shift(1)
    data['mid_MA'] = data['Close'].rolling(window=mid).mean().shift(1)
    data['long_MA'] = data['Close'].rolling(window=long).mean().shift(1)
    data['cumulative_cost'] = init
    data['shares'] = 0
    data['signal'] = 0
    data['rest_money'] = 0
    data.loc[(data['short_MA'] >= data['mid_MA']) & (data['mid_MA'] >= data['long_MA']), 'signal'] = 1
    data.loc[(data['short_MA'] <= data['mid_MA']) & (data['mid_MA'] <= data['long_MA']), 'signal'] = -1
    data.dropna()

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

def ma_backtest_result(request):
    if request.method == 'POST':
        strategy_type = 'Moving Average'
        ticker = request.POST['ticker']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        init = int(request.POST['initial_money'])
        short_ma = int(request.POST['short_ma'])
        mid_ma = int(request.POST['mid_ma'])
        long_ma = int(request.POST['long_ma'])
        buy_condition_parms = [short_ma, mid_ma, long_ma]
        sell_condition_parms = [short_ma, mid_ma, long_ma]
        return_data = cal_ma_return(ticker, init, buy_condition_parms, sell_condition_parms, start_date, end_date)
        buy_condition = 'when {} days MA is above {} days MA and {} days MA'.format(short_ma, mid_ma, long_ma)
        sell_condition = 'when {} days MA is below {} days MA and {} days MA'.format(short_ma, mid_ma, long_ma)
        total_cost = return_data['cumulative_cost'].iloc[-1]
        total_revenue = round(return_data['amount'].iloc[-1] - init,2)
        price_movement_image = generate_price_movement_image(return_data)
        cost_revenue_image = generate_cost_revenue_image(return_data)
        return render(request, 'investment/backtest/backtest_results.html', {'ticker': ticker, 'strategy_type': strategy_type,
                'start_date': start_date, 'end_date': end_date,
                'buy_condition': buy_condition, 'sell_condition': sell_condition,
                'initial_money' : init, 'total_cost': total_cost, 'total_revenue': total_revenue,
                'price_movement_image': price_movement_image, 'cost_revenue_image': cost_revenue_image})
    else:
        return redirect('ma_backtest')