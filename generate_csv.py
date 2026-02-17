import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()

API_KEY = os.getenv("ALPHA_KEY")

def get_stock_data(symbol):

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey={API_KEY}"
    r = requests.get(url)
    data = r.json()
    
    data = data["Monthly Adjusted Time Series"]
    stock_data = []
    for timestamp, values in data.items():
        close_price = values.get("4. close")

        stock_data.append({
            "symbol": symbol,
            "timestamp": timestamp,
            "close": close_price
        })
    return stock_data

def generate_csv():
    stocks = {"NVDA": 0, "TSLA": 0, "AAPL": 0, "INTC": 0, "AMZN": 0}
    
    all_stock_data = []
    for symbol in stocks.keys():
        stock_data = get_stock_data(symbol)
        all_stock_data.extend(stock_data)
    
    df = pd.DataFrame(all_stock_data)
    
    df = df[["symbol", "timestamp", "close"]]
    
    print(df)
    
    csv_filename = "stock_prices.csv"
    df.to_csv(csv_filename, index=False)

if __name__ == "__main__":
    generate_csv()
