from django.shortcuts import render, redirect
from investment.models import StockData
import pandas as pd


# Create your views here.
# def cal_avg_return(ticker, days, amount, start_date = None, end_date = None):
#     data = get_data_from_db(ticker, start_date, end_date)
#     choosen_day = days
#     monthly_amount = amount
#     filtered_data = data.copy()
#     filtered_data['shares'] = 0
#     filtered_data.loc[filtered_data['Day'] == choosen_day, 'shares'] = monthly_amount // (filtered_data.loc[filtered_data['Day'] == choosen_day, 'Close'])
#     filtered_data['cost'] = filtered_data['shares'] * filtered_data['Close']
#     filtered_data['cumulative_shares'] = filtered_data['shares'].cumsum()
#     filtered_data['amount'] = filtered_data['cumulative_shares'] * filtered_data['Close']
#     filtered_data['cumulative_cost'] = filtered_data['cost'].cumsum()
#     filtered_data['return'] = filtered_data['amount'] - filtered_data['cumulative_cost']
#     return filtered_data

def get_data_from_db(ticker, start_date = None, end_date = None):
    ticker = ticker.upper()
    if start_date and end_date:
        data = StockData.objects.filter(Ticker=ticker, Date__range=[start_date, end_date]).order_by('Date')
    else:
        data = StockData.objects.filter(Ticker=ticker).order_by('Date')
    data = pd.DataFrame(list(data.values()))
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    data = data.reindex(columns=['Ticker', 'Date', 'Year', 'Month', 'Day', 'Open', 'High', 'Low', 'Close', 'Volume'])
    return data

def buy_condition(row):
    return row['Day'] == 10

def cal_avg_return(ticker, start_date, end_date, amount, buy_condition, sell_condition):
    # 從資料庫中獲取股票數據
    data = get_data_from_db(ticker, start_date, end_date)
    
    # 初始化必要的變數
    filtered_data = data.copy()
    filtered_data['shares'] = 0
    buy_signal = False
    
    # 遍歷每一天的數據
    for index, row in filtered_data.iterrows():
        if buy_signal and sell_condition(row):
            # 如果滿足賣出條件且已經購買股票，則賣出股票
            filtered_data.loc[index, 'shares'] = 0
            buy_signal = False
        elif not buy_signal and buy_condition(row):
            # 如果滿足購買條件且尚未購買股票，則購買股票
            shares_to_buy = amount // row['Close']
            filtered_data.loc[index, 'shares'] = shares_to_buy
            buy_signal = True
    
    # 計算資金變化
    filtered_data['cost'] = filtered_data['shares'] * filtered_data['Close']
    filtered_data['cumulative_shares'] = filtered_data['shares'].cumsum()
    filtered_data['amount'] = filtered_data['cumulative_shares'] * filtered_data['Close']
    filtered_data['cumulative_cost'] = filtered_data['cost'].cumsum()
    filtered_data['return'] = filtered_data['amount'] - filtered_data['cumulative_cost']
    
    return filtered_data

def backtest(request):
    return render(request, 'backtest.html')

def avg_backtest(request):
    return render(request, 'investment/backtest/avg_backtest_page.html')