import csv
import requests
import mb_scraper as mb
import pandas as pd
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

def get_ratios(ticker):
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=LCQXGOLSHVGOGRKF'
    r = requests.get(url)
    data = r.json()
    return data

def get_last_earnings_date(data):
    '''
    This function returns the most recent reported earnings date
    :param data:
    :return:
    '''
    # Extract reported dates
    reported_dates = [entry['reportedDate'] for entry in data['quarterlyEarnings']]
    # Find the latest date
    last_earnings_date = max(reported_dates)
    print(f'Last earnings date: {last_earnings_date}')
    # Convert it back to a string
    return last_earnings_date

def calc_future_eps(ticker, earnings):
    """
    
    :param ticker: Ticker to calculate
    :param earnings: Earnings data from Alpha Vantage API
    :return:
    """
    eps = []
    # Get last year reported EPS from Alpha Vantage API
    last_year = str(datetime.datetime.now().year - 1)
    for item in earnings['annualEarnings']:
        if last_year in item['fiscalDateEnding']:
           eps.append(item['reportedEPS'])
    # Set Year 1 and Year 2 EPS projected value from Market Beat
    eps.append(mb.get_eps(ticker,int(last_year)+1))
    eps.append(mb.get_eps(ticker,int(last_year)+2))
    print(eps)
# TODO: Implement EPS calculations for Year 3,4 and 5

ticker = input(f'Which ticker do you want to check?')
column_list = ['Date','Brokerage','Old Price Target','Price Target']
earnings_list = get_earnings_data(ticker)
#print(earnings_list)
# Filter the analyst forecasts that are after last earnings date
analyst_forecast = mb.get_stock_forecast(ticker)
analyst_forecast = mb.filter_after_earnings(analyst_forecast,get_last_earnings_date(earnings_list))

# Calculate the median of 'Price Target'
analyst_forecast['Price Target'] = pd.to_numeric(analyst_forecast['Price Target'], errors='coerce')
median_price_target = analyst_forecast['Price Target'].median()
print(f"{ticker} Median Price Target: {median_price_target}")
print(f'Max buy price based on 15%pa for 3 years: ${median_price_target/(1.15**3):.2f}')
print(analyst_forecast[column_list])

calc_future_eps(ticker, earnings_list)

ratio = get_ratios(ticker)
print(ratio['TrailingPE'])