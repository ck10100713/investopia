import pandas as pd
import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investopia.settings')
django.setup()

from investment.models import StockData

def delete_data(ticker):
    ticker = ticker.upper()
    StockData.objects.filter(Ticker=ticker).delete()

if __name__ == '__main__':
    ticker = sys.argv[1].upper()
    print("Deleting data for {}".format(ticker))
    try:
        if ticker == 'ALL':
            StockData.objects.all().delete()
            print("All data has been deleted")
            sys.exit()
        else:
            delete_data(ticker)
            print("Data for {} has been deleted".format(ticker))
    except Exception as e:
        print("Error deleting data for {}: {}".format(ticker, e))