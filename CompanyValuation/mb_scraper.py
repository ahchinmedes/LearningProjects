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

    # Clean and filter the "Date" column for valid dates in 2024
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%m/%d/%Y')

    # Filter for dates in the year 2024
    df = df[df['Date'].dt.year == 2024]
    # Apply the cleaning function to 'Analyst Name' column
    df['Analyst Name'] = clean_analyst_names(df['Analyst Name'])
    df['Brokerage'] = clean_analyst_names(df['Brokerage'])

    return df


# Ask the user for a stock ticker
ticker = input("Enter a company stock ticker: ").upper()

# Get the forecast data
forecast_df = get_stock_forecast(ticker)

# Display the DataFrame if the data was found
if forecast_df is not None:
    print(forecast_df)
    # You can also save the DataFrame to a CSV file if needed
    forecast_df.to_csv(f'{ticker}_forecast.csv', index=False)
