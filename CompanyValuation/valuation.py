import csv
import requests
import datetime

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
    url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey=LCQXGOLSHVGOGRKF'
    r = requests.get(url)
    data = r.json()
    return data


def get_latest_earnings_date(data):
    '''
    This function returns the most recent reported earnings date
    :param data:
    :return:
    '''
    # Extract reported dates
    reported_dates = [entry['reportedDate'] for entry in data['quarterlyEarnings']]
    # Find the latest date
    latest_date = max(reported_dates)
    # Convert it back to a string
    return latest_date

data = get_earnings_data('GOOGL')
print(get_latest_earnings_date(data))