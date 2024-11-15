import requests
import os
import json
from datetime import datetime
from environs import Env

env = Env()
env.read_env()
apikey1 = env.str("alpha_apikey1")



def get_future_earnings_date():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    CSV_URL = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={apikey1}'
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
            
def check_file_exist(folder, ticker, type):
    # Define file path for the local JSON data
    if type == 'prices':
        file_path = f'{folder}/{ticker}_{type}.json'
    else:
        file_path = f'{folder}/{ticker}/{ticker}_{type}.json'
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
    print(apikey1)
    
    # Check if the file already exists
    data = check_file_exist('Output_Files', ticker,'earnings')
    if data is not None:
        # Existing recent data found
        return data
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={apikey1}'
    r = requests.get(url)
    data = r.json()
   # save json file to local drive
    save_data_to_local('Output_Files', data, ticker, 'earnings')
    return data

def check_valid_data(data, ticker):
    try:
        if "thank you" in data['Information'].lower():
            print(f'Invalid data in {ticker}')
            return {}
    except KeyError:
        # Return data if KeyError occurs
        return data
    

def get_price(ticker):
    # Define file path for the local JSON data
    print(apikey1)
    # Check if the file already exists
    data = check_file_exist('Daily_Prices', ticker, 'prices')
    # TODO: create new function to check for thank you msg
    if data is not None:
        # Existing recent data found. Check if "Thank you" is in the Information field
        try:
            if "thank you" in data['Information'].lower():
                print(f'Invalid data in {ticker}')
                return {}
        except KeyError:
            # Return data if KeyError occurs
            return data

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={apikey1}'
    r = requests.get(url)
    data = r.json()
    if data is not None:
        # Existing recent data found. Check if "Thank you" is in the Information field
        try:
            if "thank you" in data['Information'].lower():
                print(f'Invalid data in {ticker}')
                return {}
        except KeyError:
            # save json file to local drive
            save_data_to_local('Daily_Prices', data, ticker, 'prices')
            # Return data if KeyError occurs
            return data
    return data

def save_data_to_local(folder, data, ticker, type):
    # Define file path for the local JSON data
    if type == 'prices':
        file_path = f'{folder}/{ticker}_{type}.json'
    else:
        file_path = f'{folder}/{ticker}/{ticker}_{type}.json'
    # Save the data to a local JSON file with the query date
    with open(file_path, 'w') as f:
        json.dump({'queryDate': datetime.today().strftime('%Y-%m-%d'), 'data': data}, f)
    print(f"{type} for {ticker} has been updated and saved.")

def get_ratios(ticker):
    data = check_file_exist('Output_Files', ticker,'ratios')
    if data is not None:
        # Existing recent data found
        return data
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=apikey1'
    r = requests.get(url)
    data = r.json()
    # save json file to local drive
    save_data_to_local('Output_Files', data, ticker, 'ratios')
    return data

    
def main():
    stock_list = ['AMD','PFE','AMZN','GOOGL',"IWM",'APA','SLB','XLE','FTNT','NVDA','JPM','PLTR','TLT','SPY']
    indices = ['XLB','XLC','XLE','XLF','XLI','XLK','XLP','XLRE','XLU','XLV','XLY','TLT','FXI','SMH','XRT','GLD','SLV','INDA','JETS','SPY']
    test = ['INDA','XRT']
    for i in test:
       get_price(i)
       

if __name__ == '__main__':
    main()
    