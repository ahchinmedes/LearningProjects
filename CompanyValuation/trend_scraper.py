import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt

def get_soup(ticker):
	"""
	This function returns the Soup object after pinging the Marketbeat website
	:param ticker: Stock ticker to query
	:param exchange: Exchange for ticker
	:param type: website page. Can be forecast, earnings, etc
	:return: Soup object
	"""
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
	}
	url_maker = {'GOOGL':'alphabet','MSFT':'microsoft', 'AMZN':'amazon','AMD':'amd','PLTR':'palantir-technologies'}
	# Define the URL using the user input ticker
	url = f'https://www.macrotrends.net/stocks/charts/{ticker}/{url_maker.get(ticker)}/pe-ratio'
	# Send a GET request to fetch the page content
	response = requests.get(url, headers=headers)
	# Check if the request was successful
	if response.status_code != 200:
		print(f"Failed to retrieve data for . Status code: {response.status_code}")
		return None
	# Parse the page content using BeautifulSoup
	return BeautifulSoup(response.content, 'html.parser')

def scrape_pe(ticker):
	"""
	This function scrapes the Microtrends website for PE table and store it in a DataFrame
	:param ticker:
	:return: DataFrame storing all the PE information from website
	"""
	soup1 = get_soup(ticker)
	# Find the heading that precedes the table
	heading = soup1.find('th', string=re.compile('PE Ratio Historical Data'))
	# Find the table that follows this heading
	table = heading.find_parent('table')
	
	# Extract headers
	headers = []
	for th in table.find_all('th'):
		headers.append(th.text.strip())
	
	# Extract rows from the table body
	rows = []
	for tr in table.find('tbody').find_all('tr'):
		cells = tr.find_all('td')
		row = [cell.text.strip() for cell in cells]
		rows.append(row)
	
	# Convert to DataFrame for easier manipulation
	del headers[0] # 1st element is main header "PE Ratio Historical Data"
	df = pd.DataFrame(rows, columns=headers)
	
	# Clean data
	# Remove $ from numbers, and set empty strings as 0
	df['TTM Net EPS'] = df['TTM Net EPS'].replace({r'\$': '', '': 0}, regex=True)
	
	# set data type for df
	df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
	df.sort_values('Date',ascending=False, inplace=True)
	df['Stock Price'] = df['Stock Price'].astype('float')
	df['TTM Net EPS'] = df['TTM Net EPS'].astype('float')
	df['PE Ratio'] = df['PE Ratio'].astype('float')
	return df

def calculate_pe(df):
	"""
	This function calculates the min and average PE of the last 7 years using MacroTrend data
	:param df:
	:return: min pe, average pe, DataFrame (last 7 years)
	"""
	# Define the date for 7 years ago
	seven_years_ago = df['Date'][0] - pd.DateOffset(years=7)
	# Filter rows where Date is within the last 7 years
	df_filtered = df[df['Date'] >= seven_years_ago]
	# Calculate min and average PE of last 7 years (estimated)
	min_pe = df_filtered['PE Ratio'].min()
	max_pe = df_filtered['PE Ratio'].max()
	if max_pe - min_pe > 100:
		# Use quartile if range of PE is too wide, ie more than 100
		min_pe = df_filtered['PE Ratio'].quantile(0.10)
		ave_pe = df_filtered['PE Ratio'].quantile(0.60)
	else:
		ave_pe = (max_pe - min_pe) * 0.4 + min_pe
	return min_pe, ave_pe, df_filtered

def main():
	ticker = 'GOOGL'
	min_pe, ave_pe, df = calculate_pe(scrape_pe(ticker))
	print(df)
	print(f'Min pe: {min_pe}')
	print(f'Ave pe: {ave_pe}')
	df.plot.line(x='Date', y= 'PE Ratio')
	plt.title(f'PE Ratio of {ticker}')
	plt.show()

if __name__ == '__main__':
	main()