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
    file_path = f'Output_Files/{ticker}_earnings.json'
    
    # Check if the file already exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            local_data = json.load(f)
            
            # Check the date of the last query
            last_query_date = local_data.get('queryDate')
            if last_query_date:
                last_query_date = datetime.strptime(last_query_date, '%Y-%m-%d')
                today = datetime.today()
                
                # If the data is from the same month and year, return the local data
                if last_query_date.year == today.year and last_query_date.month == today.month:
                    print(f"Using cached data for {ticker}")
                    return local_data['data']
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey=LCQXGOLSHVGOGRKF'
    r = requests.get(url)
    data = r.json()
    
    # Save the data to a local JSON file with the query date
    with open(file_path, 'w') as f:
        json.dump({'queryDate': datetime.today().strftime('%Y-%m-%d'), 'data': data}, f)
    print(f"Data for {ticker} has been updated and saved.")
    
    return data

def get_ratios(ticker):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=LCQXGOLSHVGOGRKF'
    r = requests.get(url)
    data = r.json()
    return data