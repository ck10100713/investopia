from django.shortcuts import render, redirect
from investment.models import StockData
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# graphic parms
plt_size = (10, 5)

# Create your views here.
def bb_backtest(request):
    return render(request, 'investment/backtest/bb_backtest_page.html')

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

def get_data_from_db_before_date(ticker, date, ma):
    ticker = ticker.upper()
    data = StockData.objects.filter(Ticker=ticker, Date__lt=date).order_by('-Date')[:ma]
    data = pd.DataFrame(list(data.values()))
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    data = data.reindex(columns=['Ticker', 'Date', 'Year', 'Month', 'Day', 'Open', 'High', 'Low', 'Close', 'Volume'])
    return data

def backtest(request):
    return render(request, 'backtest.html')

def bb_backtest(request):
    return render(request, 'investment/backtest/bb_backtest_page.html')

def generate_price_movement_image(data):
    plt.figure(figsize=plt_size)
    plt.plot(data['Date'], data['Close'], label='Close Price', color='black')
    plt.scatter(data[data['shares'] > 0]['Date'], data[data['shares'] > 0]['Close'], marker='^', color='green', label='Buy Signal', s=50)
    plt.scatter(data[data['shares'] < 0]['Date'], data[data['shares'] < 0]['Close'], marker='v', color='red', label='Sell Signal', s=50)
    # plt.scatter(filtered_data[filtered_data['shares'] == 0]['Date'], filtered_data[filtered_data['shares'] == 0]['Close'], marker='v', color='red')
    plt.title('Dollar Cost Averaging')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    image_data = f"data:image/png;base64,{image_base64}"
    return image_data

def generate_cost_revenue_image(data):
    plt.figure(figsize=plt_size)
    plt.plot(data['Date'], data['cumulative_cost'], label='Cumulative Cost', color='blue')
    plt.plot(data['Date'], data['amount'], label='Amount', color='red')
    plt.title('Dollar Cost Averaging')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.legend()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    image_data = f"data:image/png;base64,{image_base64}"
    return image_data

def cal_bb_return(ticker, ma, buy_condition, sell_condition, start_date = None, end_date = None):
    # get previous ma data before start_date
    previous_data = get_data_from_db_before_date(ticker, start_date, ma)
    data = get_data_from_db(ticker, start_date, end_date)
    # concat data
    data = pd.concat([previous_data, data], axis=0)
    data.sort_values(by='Date', inplace=True)
    data = data.reset_index()
    filtered_data = data.copy()
    filtered_data['MA'] = filtered_data['Close'].rolling(window=ma).mean().shift(1)
    filtered_data['std'] = filtered_data['Close'].rolling(window=ma).std().shift(1)
    filtered_data['upper_band'] = filtered_data['MA'] + (filtered_data['std'] * buy_condition[1])
    filtered_data['lower_band'] = filtered_data['MA'] - (filtered_data['std'] * buy_condition[1])
    filtered_data['shares'] = 0
    filtered_data['signal'] = 0
    filtered_data['cumulative_shares'] = 0
    filtered_data['cumulative_cost'] = 0
    filtered_data.loc[(filtered_data['MA'] >= 0) & (filtered_data['Close'] > filtered_data['upper_band']), 'signal'] = 1
    filtered_data.loc[(filtered_data['MA'] >= 0) & (filtered_data['Close'] < filtered_data['lower_band']), 'signal'] = -1

    shares = 0
    profit = 0
    cost = 0
    for i in range(len(filtered_data)):
        if filtered_data.iloc[i]['signal'] == 1 and shares == 0:
            shares += 1
            cost = filtered_data.iloc[i]['Close']
            filtered_data.loc[i, 'shares'] = 1
        elif filtered_data.iloc[i]['signal'] == -1 and shares > 0:
            shares -= 1
            profit += filtered_data.iloc[i]['Close'] - cost
            cost = 0
            filtered_data.loc[i, 'shares'] = -1
        filtered_data.loc[i, 'cumulative_shares'] = shares
        filtered_data.loc[i, 'cumulative_cost'] = cost
    filtered_data.dropna(inplace=True)
    filtered_data['amount'] = filtered_data['cumulative_shares'] * filtered_data['Close']
    # print(filtered_data[['Date', 'Close', 'MA', 'upper_band', 'lower_band', 'shares', 'signal']].head(50))
    return filtered_data

def bb_backtest_result(request):
    if request.method == 'POST':
        strategy_type = 'Bollinger Band'
        ticker = request.POST['ticker']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        ma = int(request.POST['ma'])
        std = int(request.POST['std'])
        buy_condition = [ma, std]
        sell_condition = [ma, std]
        return_data = cal_bb_return(ticker, ma, buy_condition, sell_condition, start_date, end_date)

        total_cost = return_data['cumulative_cost'].iloc[-1]
        total_revenue = return_data['amount'].iloc[-1]
        price_movement_image = generate_price_movement_image(return_data)
        cost_revenue_image = generate_cost_revenue_image(return_data)
        return render(request, 'investment/backtest/backtest_results.html', {'ticker': ticker, 'strategy_type': strategy_type,
                'start_date': start_date, 'end_date': end_date,
                'buy_condition': buy_condition, 'sell_condition': sell_condition,
                'total_cost': total_cost, 'total_revenue': total_revenue,
                'price_movement_image': price_movement_image, 'cost_revenue_image': cost_revenue_image})
    else:
        return redirect('bb_backtest')