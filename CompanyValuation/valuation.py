import csv
import mb_scraper as mb
import alpha_api as alpha
import finviz_scraper as fv
import pandas as pd
from _datetime import datetime
import generate_pdf as p

def get_last_earnings_date(data):
    """
    This function returns the most recent reported earnings date.
    Source of data is JSON output from Alpha Vantage API
    :param data: Dictionary format with keys "annualEarnings" and "quarterlyEarnings"
    :return: latest reported earnings date
    """
    # Extract reported dates
    reported_dates = [datetime.strptime(entry['reportedDate'],'%Y-%m-%d') for entry in data['quarterlyEarnings']]
    # Find the latest date
    last_earnings_date = max(reported_dates)
    print(f'Last earnings date: {last_earnings_date}')
    # Convert it back to a string
    return last_earnings_date

def calc_future_eps():
    """
    This function sets last year reported EPS value from Alpha Vantage API as eps[0]
    Year 1 and 2 - eps[1:3] will be EPS value scraped from Market Beat Earnings website, which are projected values
    Year 3 to 5 - eps[3:6] will be calculated using EPS growth rate scraped from fv website
    Max buy price is calculated from getting projected price at Year 3 (2 years later) and
    divide by 1.3 (assume 15% x 2 years return)
    :param ticker: Ticker to calculate
    :param earnings: Earnings data from Alpha Vantage API
    :return:
    """
    eps = []
    # Get last year reported EPS from Alpha Vantage API and store as eps[0]
    last_year = str(datetime.now().year - 1)
    eps.extend([float(item['reportedEPS']) for item in earnings_list['annualEarnings'] if last_year in item['fiscalDateEnding']])
    
    # Set Year 1 and Year 2 EPS projected value from Market Beat
    eps.extend([float(mb.get_eps(ticker, int(last_year) + i)) for i in range(1, 3)])
    
    # Compute eps for year 3 to 5 by multiplying year 3 with eps growth rate
    eps_growth = 1+fv.get_value(fv_data,'EPS next 5Y')/100
    print(f'5Y EPS Growth: {eps_growth:2f}')
    eps.extend([round(eps[2] * eps_growth**(i+1), 2) for i in range(3)])
    print(eps)
    pe = float(fv.get_value(fv_data,'P/E'))
    print(f'Current P/E: {pe}')
    price_forecast = [round(e * pe,2) for e in eps]
    price_forecast[0] = current_price
    print(price_forecast)
    # Assuming holding 2 years at 15% pa, ie divide by 30%
    print(f'Max Buy Price: $ {price_forecast[2]/1.3:.2f}')
    
def generate_pdf():
    p.print_fundamentals(pdf, current_price,fv_data['P/E'].values[0], fv_data['EPS next 5Y'].values[0])
    p.save_pdf(pdf)




ticker = input(f'Which ticker do you want to check?')
#ticker = 'BABA'
fv_data = fv.scrape_finviz_data(ticker)
pdf = p.create_pdf(ticker)
current_price = fv.scrape_current_stock_price(ticker)
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
mbp = round(median_price_target/(1.15**3),2)
print(f'Max buy price based on 15%pa for 3 years: ${mbp}\n')
analyst_filtered = analyst_forecast[column_list]
p.print_analyst_buy(pdf, analyst_filtered,get_last_earnings_date(earnings_list),median_price_target,mbp)

print(analyst_filtered)

calc_future_eps()
generate_pdf()

# ratio = get_ratios(ticker)
# print(ratio['TrailingPE'])