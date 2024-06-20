from django.shortcuts import render, redirect
from investment.models import StockData
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

plt_size = (10, 5)

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

def backtest(request):
    return render(request, 'backtest.html')

def avg_backtest(request):
    return render(request, 'investment/backtest/avg_backtest_page.html')

def generate_price_movement_image(data):
    plt.figure(figsize=plt_size)
    plt.plot(data['Date'], data['Close'], label='Close Price', color='black')
    plt.scatter(data[data['shares'] > 0]['Date'], data[data['shares'] > 0]['Close'], marker='^', color='green', label='Buy Signal', s=50)
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

def cal_avg_return(ticker, amount, buy_condition, sell_condition, start_date = None, end_date = None):
    data = get_data_from_db(ticker, start_date, end_date)
    monthly_amount = amount
    filtered_data = data.copy()
    filtered_data['shares'] = 0
    filtered_data.loc[filtered_data['Day'] == buy_condition, 'shares'] = monthly_amount // (filtered_data.loc[filtered_data['Day'] == buy_condition, 'Close'])
    filtered_data['cost'] = filtered_data['shares'] * filtered_data['Close']
    filtered_data['cumulative_shares'] = filtered_data['shares'].cumsum()
    filtered_data['amount'] = filtered_data['cumulative_shares'] * filtered_data['Close']
    filtered_data['cumulative_cost'] = filtered_data['cost'].cumsum()
    filtered_data['return'] = filtered_data['amount'] - filtered_data['cumulative_cost']
    return filtered_data

def avg_backtest_result(request):
    if request.method == 'POST':
        strategy_type = 'Dollar Cost Averaging'
        ticker = request.POST['ticker']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        amount = float(request.POST['amount'])
        buy_condition = int(request.POST['days'])
        sell_condition = None
        return_data = cal_avg_return(ticker, amount, buy_condition, sell_condition, start_date, end_date)
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
        return redirect('avg_backtest')