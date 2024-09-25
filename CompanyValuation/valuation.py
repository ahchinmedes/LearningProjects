import csv
import mb_scraper as mb
import alpha_api as alpha
import finviz_scraper as finviz
import pandas as pd
import datetime



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

def calc_future_eps(ticker, earnings, finviz_data):
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
           eps.append(float(item['reportedEPS']))
           
    # Set Year 1 and Year 2 EPS projected value from Market Beat
    eps.extend([float(mb.get_eps(ticker, int(last_year) + i)) for i in range(1, 3)])
    
    # Compute eps for year 4 to 6 by multiplying year 3 with eps growth rate
    eps_growth = 1+finviz.get_value(finviz_data,'EPS next 5Y')/100
    print(f'5Y EPS Growth: {eps_growth:2f}')
    eps.extend([round(eps[2] * eps_growth**(i+1), 2) for i in range(3)])
    print(eps)
    pe = float(finviz.get_value(finviz_data,'P/E'))
    print(f'Current P/E: {pe}')
    price_forecast = [round(e * pe,2) for e in eps]
    print(price_forecast)
    print(f'Max Buy Price: $ {price_forecast[2]/1.3:.2f}')

ticker = input(f'Which ticker do you want to check?')
column_list = ['Date','Brokerage','Old Price Target','Price Target']
earnings_list = alpha.get_earnings_data(ticker)
#print(earnings_list)
# Filter the analyst forecasts that are after last earnings date
analyst_forecast = mb.get_stock_forecast(ticker)
analyst_forecast = mb.filter_after_earnings(analyst_forecast,get_last_earnings_date(earnings_list))

# Calculate the median of 'Price Target'
analyst_forecast['Price Target'] = pd.to_numeric(analyst_forecast['Price Target'], errors='coerce')
median_price_target = analyst_forecast['Price Target'].median()
print(f"{ticker} Median Price Target: {median_price_target}")
print(f'Max buy price based on 15%pa for 3 years: ${median_price_target/(1.15**3):.2f}\n')

print(analyst_forecast[column_list])

finviz_data = finviz.scrape_finviz_data(ticker)
calc_future_eps(ticker, earnings_list,finviz_data)

# ratio = get_ratios(ticker)
# print(ratio['TrailingPE'])