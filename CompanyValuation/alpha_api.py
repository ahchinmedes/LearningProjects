import requests
import os
import json
from datetime import datetime

def get_future_earnings_date():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    CSV_URL = 'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey=LCQXGOLSHVGOGRKF'
    my_tickers = ['AMD','NVDA','AAPL','AMZN','GOOGL']
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        # returns values in this header ['symbol', 'name', 'reportDate', 'fiscalDateEnding', 'estimate', 'currency']
        my_list = list(cr)
        for row in my_list:
          if row[0] in my_tickers:
            print(row)
            
def check_file_exist(ticker, type):
    # Define file path for the local JSON data
    file_path = f'Output_Files/{ticker}/{ticker}_{type}.json'
    if os.path.exists(file_path):
        # Open file if file exist
        with open(file_path, 'r') as f:
            local_data = json.load(f)
            # Check the date of the last query
            last_query_date = local_data.get('queryDate')
            if last_query_date:
                last_query_date = datetime.strptime(last_query_date, '%Y-%m-%d')
                today = datetime.today()
                # If the data is from the same month and year, return the local data
                if last_query_date.year == today.year and last_query_date.month == today.month:
                    print(f"Alpha Vantage API: Using cached data for {ticker}")
                    return local_data['data']
    # File not exist or not last query not in this month
    print(f'Alpha Vantage API: No local data found for {type}, trigger API call...')
    return None

def get_earnings_data(ticker):
    """
    Obtain JSON data from API and stores in local file with query date. If local file exists and query
    date is within 1 month, use local file details to save on API daily limit.
    Sample format below
    
    "symbol": "IBM",
    "annualEarnings": [
        {
            "fiscalDateEnding": "2024-06-30",
            "reportedEPS": "4.11"
        },
    "quarterlyEarnings": [
        {
            "fiscalDateEnding": "2024-06-30",
            "reportedDate": "2024-07-24",
            "reportedEPS": "2.43",
            "estimatedEPS": "2.2",
            "surprise": "0.23",
            "surprisePercentage": "10.4545",
            "reportTime": "post-market"
        },
    :param ticker: Stock ticker to query
    :return: Dictionary of data
    """
    # Define file path for the local JSON data
    
    # Check if the file already exists
    data = check_file_exist(ticker,'earnings')
    if data is not None:
        # Existing recent data found
        return data
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey=LCQXGOLSHVGOGRKF'
    r = requests.get(url)
    data = r.json()
   # save json file to local drive
    save_data_to_local(data, ticker, 'earnings')
    return data

def save_data_to_local(data, ticker, type):
    # Define file path for the local JSON data
    file_path = f'Output_Files/{ticker}/{ticker}_{type}.json'
    # Save the data to a local JSON file with the query date
    with open(file_path, 'w') as f:
        json.dump({'queryDate': datetime.today().strftime('%Y-%m-%d'), 'data': data}, f)
    print(f"{type} for {ticker} has been updated and saved.")

def get_ratios(ticker):
    data = check_file_exist(ticker,'ratios')
    if data is not None:
        # Existing recent data found
        return data
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=LCQXGOLSHVGOGRKF'
    r = requests.get(url)
    data = r.json()
    # save json file to local drive
    save_data_to_local(data, ticker, 'ratios')
    return data

def get_stock_daily_price(ticker):
    data = check_file_exist(ticker,'prices')
    if data is not None:
        # Existing recent data found
        return data
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey=LCQXGOLSHVGOGRKF'
    r = requests.get(url)
    data = r.json()
    # save json file to local drive
    save_data_to_local(data, ticker, 'prices')
    
def main():
    get_stock_daily_price('AMD')

if __name__ == '__main__':
    main()
    