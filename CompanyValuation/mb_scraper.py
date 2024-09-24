import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def clean_analyst_names(analyst_names):
   cleaned_names = []
   for name in analyst_names:
       # Remove "x of 5 stars" if found
       name = re.sub(r'\s*\d+ of \d+ stars', '', name)
       # Remove "Subscribe" and anything following it
       name = re.sub(r'\s*Subscribe.*', '', name).strip()
       # Append the cleaned name
       cleaned_names.append(name)
   return cleaned_names

def extract_price_targets(price_target):
    """
    This function extracts 2 numbers from the website.
    For example: $132 -> $140
    $132 will be stored as old price, $140 will be stored as new price.
    :param price_target:
    :return: old price, new price if found
    """
    match = re.match(r'\$(\d+(\.\d+)?) ➝ \$(\d+(\.\d+)?)', price_target)
    if match:
        old_price, new_price = match.groups()[0], match.groups()[2]
        return old_price, new_price
    return None, None

def filter_after_earnings(df, date):
    """
    Filter the DataFrame for rows where 'Date' is after date
    :param df: contains all the historical earnings date
    :param date: most recent earnings date
    :return: filtered df
    """
    filtered_df = df[df['Date'] >= date]
    return filtered_df

def get_stock_forecast(ticker):
    # Define the URL using the user input ticker
    url = f'https://www.marketbeat.com/stocks/NASDAQ/{ticker}/forecast/'
    # Send a GET request to fetch the page content
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for {ticker}. Status code: {response.status_code}")
        return None
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the section that starts with the "Recent Analyst Forecasts and Stock Ratings" heading
    ratings_table_section = soup.find('h2', {'id': 'ratings-table'})
    if not ratings_table_section:
        print(f"No ratings table found for {ticker}")
        return None
    # The table is typically located right after this section
    table = ratings_table_section.find_next('table', {'class': 'scroll-table'})
    if not table:
        print(f"No forecast data found for {ticker}")
        return None
    # Extract table headers
    headers = [header.text.strip() for header in table.find_all('th')]
    # Extract table rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = [col.text.strip() for col in row.find_all('td')]
        if cols:
            rows.append(cols)

    # Create a DataFrame from the table data
    df = pd.DataFrame(rows, columns=headers)
    
    # Data Cleaning Section
    # Apply the cleaning function to 'Analyst Name' column
    df['Analyst Name'] = df['Analyst Name'].fillna('')
    df['Brokerage'] = df['Brokerage'].fillna('')
    df['Price Target'] = df['Price Target'].fillna('')
    df['Analyst Name'] = clean_analyst_names(df['Analyst Name'])
    df['Brokerage'] = clean_analyst_names(df['Brokerage'])
    #Convert 'Date' to datetime, invalid parsing will result in NaT
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    #Remove rows with invalid dates (NaT)
    df = df[df['Date'].notna()]
    df['Old Price Target'] = None
    # Apply the extraction function to 'Price Target' column
    df[['Old Price Target', 'Price Target']] = df['Price Target'].apply(lambda x: pd.Series(extract_price_targets(x)))
    return df

def scrape_eps_estimates(ticker):
    """
    This function scraps the website and returns the
    Headers: ['Quarter', 'Number of Estimates', 'Low Estimate', 'High Estimate', 'Average Estimate', 'Company Guidance']
    :param ticker:
    :return:
    """
    # URL with the ticker as a variable
    url = f'https://www.marketbeat.com/stocks/NASDAQ/{ticker}/earnings/'
    # Send a GET request to the website
    response = requests.get(url)
    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for {ticker}. Status code: {response.status_code}")
        return
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the specific section by locating the h2 tag with the class 'h3' and the desired title
    section = soup.find('h2', class_='h3', string=lambda text: 'Analyst EPS Estimates' in text)
    if not section:
        print(f"No EPS estimates section found for {ticker}")
        return
    # Find the table that comes after the section
    table = section.find_next('table')
    if not table:
        print(f"No table found under EPS estimates for {ticker}")
        return
    # Extract the headers from the table
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    #print("Headers:", headers)
    # Extract the rows from the table
    rows = []
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        columns = row.find_all('td')
        data = [col.get_text(strip=True) for col in columns]
        rows.append(data)
    # Create a pandas DataFrame from the scraped data
    df = pd.DataFrame(rows, columns=headers)
    # Print or return the DataFrame for further processing
    #print(df[['Quarter','Average Estimate','Company Guidance']])
    #print(df)
    return df

def get_eps(ticker, year):
    """
    This function returns the full financial year projected EPS of a
    given year and ticker from MarketBeat website
    It will also remove "$" from the values
    :param ticker: Ticker to query
    :param year: Year to query
    :return: Full financial year EPS
    """
    eps = scrape_eps_estimates(ticker)
    # Filter the row where 'Quarter' equals 'FY ' + year
    row = eps[eps['Quarter'] == f'FY {year}']
    # Check if the row exists and return the Average Estimate
    if not row.empty:
        # Remove $ and return the digits only
        return re.sub(r'\$', '',row['Average Estimate'].values[0])
    else:
        return None

# Get the forecast data
#forecast_df = get_stock_forecast('AMD')
#print(forecast_df)
#forecast_df.to_csv(f'AMD_forecast.csv', index=False)
'''
# Display the DataFrame if the data was found
if forecast_df is not None:
    #filtered_df = filter_after_earnings(forecast_df, earnings)
    #print(forecast_df)
    print(filtered_df[['Date', 'Old Price Target', 'Price Target']])
    prices = pd.to_numeric(filtered_df['Price Target'], errors='coerce')
    print(f"Median of Price Target: {prices.dropna().median()}")

    # You can also save the DataFrame to a CSV file if needed
   # filtered_df.to_csv(f'{ticker}_forecast.csv', index=False)
'''
