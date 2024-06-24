from investment.models import StockData
import pandas as pd

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

def get_data_from_db_before_date(ticker, date, day):
    ticker = ticker.upper()
    data = StockData.objects.filter(Ticker=ticker, Date__lt=date).order_by('-Date')[:day]
    data = pd.DataFrame(list(data.values()))
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    data = data.reindex(columns=['Ticker', 'Date', 'Year', 'Month', 'Day', 'Open', 'High', 'Low', 'Close', 'Volume'])
    return data