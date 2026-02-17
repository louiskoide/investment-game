import os
from dotenv import load_dotenv
import requests
import datetime
import pandas as pd

load_dotenv()

API_KEY = os.getenv("ALPHA_KEY")

def calculate_date(months):
    start_date = datetime.datetime(2011, 1, 1)

    total_month = start_date.month + months
    
    new_year = start_date.year + (total_month - 1) // 12
    new_month = (total_month - 1) % 12 + 1
    new_date = datetime.datetime(new_year, new_month, 1)
    
    return new_date.strftime("%Y-%m")
    

def get_price(symbol, months):
    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    
    date = calculate_date(months)
    
    if "Information" not in data:
        
        data = data["Monthly Adjusted Time Series"]
        
        for key in data:
            if key.startswith(date):
                return float(data[key]["4. close"])
        
        return None
        
    else:
        df = pd.read_csv("stock_prices.csv")
    
        symbol_filter = df["symbol"] == symbol
        
        timestamp_filter = df["timestamp"].astype(str).str.startswith(date)
        
        filtered = df[symbol_filter & timestamp_filter]
        
        if not filtered.empty:
            return float(filtered.iloc[0]["close"])
        else:
            return None
        

def get_stocks(months):
    
    stocks = {"NVDA": 0, "TSLA": 0, "AAPL": 0, "INTC": 0, "AMZN": 0}
    
    for stock in stocks:
        stocks[stock] = round(float(get_price(stock, months)), 2)
    
    return stocks
    

if __name__ == "__main__":

    stocks = get_stocks(1)
    for stock in stocks:
        print(f"{stock} - {stocks[stock]}")
