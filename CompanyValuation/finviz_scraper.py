import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_finviz_data(ticker):
    # URL with the ticker as a variable
    url = f'https://finviz.com/quote.ashx?t={ticker}&p=d'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    # Send a GET request to the website
    response = requests.get(url, headers=headers)
    
    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data for {ticker}. Status code: {response.status_code}")
        return
    
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table with the specified class
    table = soup.find('table', class_='js-snapshot-table snapshot-table2 screener_snapshot-table-body')
    if not table:
        print(f"No table found for {ticker}")
        return
    
    # Extract headers and values
    headers = []
    values = []

    # Find all rows
    rows = table.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        # Iterate through columns in pairs (header, value)
        for i in range(0, len(cols), 2):
            if i + 1 < len(cols):
                header = cols[i].get_text(strip=True)
                value = cols[i + 1].get_text(strip=True)
                headers.append(header)
                values.append(value)

    # Create a DataFrame from the dictionary
    df = pd.DataFrame([values], columns=headers)

    # Print or return the DataFrame for further processing
    # print(df)
    
    # Define the filename
    filename = f'{ticker}_finviz.csv'
    # Save DataFrame to CSV file
    df.to_csv(filename, index=False)
    
    return df


# Example usage
ticker = 'AMZN'  # Replace with any ticker symbol
df = scrape_finviz_data(ticker)
#print(df['EPS next 5Y'].values[0])
#print(df)
