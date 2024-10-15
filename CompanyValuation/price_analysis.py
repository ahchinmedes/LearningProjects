from matplotlib.pyplot import subplots

import alpha_api as alpha
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_prices(ticker):
    data = alpha.get_price(ticker)
    # Extract the Time Series data
    time_series_data = data["Time Series (Daily)"]
    # Convert to DataFrame directly
    df = pd.DataFrame.from_dict(time_series_data, orient='index')
    return df

def data_clean(df,days):
    df = df.astype('float')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    if 'NVDA' in df.columns:
        # Divide 'NVDA' by 10 before '2024-06-07', retain original values after '2024-06-07'
        df['NVDA'] = np.where(df.index <= '2024-06-07', df['NVDA'] / 10, df['NVDA'])
    return df.iloc[-days:]


def calculate_rrg_tv(df, len=15):
    # Assuming the last column in the DataFrame is the benchmark (e.g., 'SPY' or 'NDX')
    stock_columns = df.columns[:-1]  # All columns except the last one
    index_column = df.columns[-1]  # The last column is the benchmark index
    
    rs_ratios = pd.DataFrame()
    rm_ratios = pd.DataFrame()
    
    for stock in stock_columns:
        # Calculate RS (Relative Strength)
        rs = (df[stock] / df[index_column]) * 100
        rs_ratio = rs.div(rs.iloc[0]).mul(100)
        
        # Calculate the Rate of Change (ROC) for rs_ratio
        rm_ratio = rs_ratio.pct_change(periods=len) * 100
       
        #trading view way of normalisation
        # Normalize RS-Ratio (JDK RS-Ratio)
        #rs_ratio = rs.rolling(window=len).mean()
        #rs_ratio_mean = rs_ratio.rolling(window=len).mean()
        #rs_ratio_std = rs_ratio.rolling(window=len).std()
        #jdk_rs_ratio = 100 + ((rs_ratio - rs_ratio_mean) / rs_ratio_std) + 1
        
        # Normalize RM-Ratio (JDK RM-Ratio)
        rm_ratio_mean = rm_ratio.rolling(window=len).mean()
        rm_ratio_std = rm_ratio.rolling(window=len).std()
        jdk_rm_ratio = 100 + ((rm_ratio - rm_ratio_mean) / rm_ratio_std) + 1
        
        # Store results for each stock
        rs_ratios[f'{stock}_rs_ratio'] = rs_ratio
        rm_ratios[f'{stock}_rm_ratio'] = jdk_rm_ratio
    
    return rs_ratios, rm_ratios

def weighted_moving_average(data, period):
    # Function to calculate WMA (Weighted Moving Average)
    weights = np.arange(1, period + 1)
    return data.rolling(window=period).apply(lambda prices: np.dot(prices, weights) / weights.sum(), raw=True)

def calculate_rrg(df, len=19):
    stock_columns = df.columns[:-1]  # All columns except the last one
    index_column = df.columns[-1]  # The last column is the benchmark index
    
    rs_ratios = pd.DataFrame()
    rm_ratios = pd.DataFrame()
    
    for stock in stock_columns:
        # Step 1: Calculate RS (Relative Strength)
        rs = df[stock] / df[index_column]
        
        # Step 2: Calculate WMA of RS for normalization
        wma_rs = weighted_moving_average(rs, len)
        
        # Step 3: Calculate RS-Ratio (normalized RS, TradingView style)
        rs_ratio = weighted_moving_average(rs / wma_rs, len) * 100
        
        # Step 4: Calculate RS-Momentum (RM-Ratio)
        rs_mom = (rs_ratio / weighted_moving_average(rs_ratio, len)) * 100
        
        # Store results for each stock
        rs_ratios[f'{stock}_rs_ratio'] = rs_ratio
        rm_ratios[f'{stock}_rm_ratio'] = rs_mom
    
    return rs_ratios, rm_ratios

def plot_RRG(rs_ratio, rs_momentum):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Define the quadrant colors
    leading_color = 'lightgreen'
    weakening_color = 'lightyellow'
    lagging_color = 'lightcoral'
    improving_color = 'lightblue'
    
    # Plot each stock's RS-Ratio and RS-Momentum
    for stock in rs_ratio.columns:
        stock_name = stock.replace('_rs_ratio', '')
        
        # Plot all points for the stock and connect them with lines
        ax.plot(rs_ratio[stock], rs_momentum[f'{stock_name}_rm_ratio'], label=stock_name, marker='o')
        
        # Add arrows for transition between points (days)
        for i in range(len(rs_ratio[stock]) - 1):
            ax.annotate('', xy=(rs_ratio[stock].iloc[i + 1], rs_momentum[f'{stock_name}_rm_ratio'].iloc[i + 1]),
                        xytext=(rs_ratio[stock].iloc[i], rs_momentum[f'{stock_name}_rm_ratio'].iloc[i]),
                        arrowprops=dict(arrowstyle="->", color='gray', lw=1))
        # Add the stock name with spacing at the last point
        #text_x = rs_ratio[stock].iloc[-1] + 0.2  # Shift name 0.5 units to the right
        #text_y = rs_momentum[f'{stock_name}_rm_ratio'].iloc[-1] + 0.2  # Shift name 0.5 units upward
        #ax.text(text_x, text_y, stock_name, fontsize=10, color='black', ha='center', va='center')
    # Set axis labels and title
    ax.set_xlabel('RS-Ratio')
    ax.set_ylabel('RS-Momentum')
    ax.set_title(f'RRG Chart ({rs_ratio.index[-1].strftime('%d/%m/%Y')})')
    
    # Set dynamic axis limits based on the range of rs_ratio and rs_momentum data
    x_min = rs_ratio.min().min() - 0.5
    x_max = rs_ratio.max().max() + 0.5
    y_min = rs_momentum.min().min() - 0.5
    y_max = rs_momentum.max().max() + 0.5
    
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    
    # Define RRG quadrants
    ax.axhline(100, color='black', linewidth=1)
    ax.axvline(100, color='black', linewidth=1)
    
    # Fill the quadrants with respective colors
    ax.fill_betweenx([100, y_max], 100, x_max, color=leading_color, alpha=0.2)  # Leading quadrant
    ax.fill_betweenx([y_min, 100], 100, x_max, color=weakening_color, alpha=0.2)  # Weakening quadrant
    ax.fill_betweenx([y_min, 100], x_min, 100, color=lagging_color, alpha=0.2)  # Lagging quadrant
    ax.fill_betweenx([100, y_max], x_min, 100, color=improving_color, alpha=0.2)  # Improving quadrant
    
    # Add quadrant labels dynamically based on axis limits
    ax.text(x_max-0.1, y_max-0.1, 'Leading', fontsize=10, color='green', ha='right', va='top')
    ax.text(x_max-1.2, y_min+0.1, 'Weakening', fontsize=10, color='orange', ha='right', va='bottom')
    ax.text(x_min+0.1, y_min+0.1, 'Lagging', fontsize=10, color='red', ha='left', va='bottom')
    ax.text(x_min+0.1, y_max-0.1, 'Improving', fontsize=10, color='blue', ha='left', va='top')
    
    # Add the legend with small font size
    plt.legend(loc='lower right', fontsize='small')
    plt.grid(True)
    
    # Show the plot
    plt.show()

def main():
    #stock_list = ['AMD','NVDA','AMZN','GOOGL','SPY']
    #stock_list = ['AMD','PFE','GOOGL','AMZN','PLTR','FTNT','NVDA','TLT','KWEB','SPY']
    stock_list = ['XLB','XLC','XLE','XLF','XLI','XLK','XLP','XLRE','XLU','XLV','XLY','SMH','XRT','GLD','SLV','SPY']
    prices_df = pd.DataFrame()
    for stock in stock_list:
        df = get_prices(stock)
        prices_df[stock] = df['4. close']
    prices_df = data_clean(prices_df,90)
    #rs_ratio, norm_price = cal_RS_Ratio(prices_df)
    # Then calculate RS-Momentum based on RS-Ratio
    #rs_momentum = cal_RS_Momentum(rs_ratio)
    # Plot RRG chart
    #plot_RRG(rs_ratio.iloc[-10:], rs_momentum.iloc[-10:])
    #rs_ratio.plot()
    #norm_price.plot()
    #plt.show()
    
    # Using Tradingview script algo
    rs_ratio, rs_momentum = calculate_rrg(prices_df)
    plot_RRG(rs_ratio.iloc[-6:],rs_momentum.iloc[-6:])
    ticker = 'XLF'
    show_stock_plot(prices_df, rs_momentum, rs_ratio, ticker)


def show_stock_plot(prices_df, rs_momentum1, rs_ratio1, ticker):
    norm_prices_df = prices_df.div(prices_df.iloc[0])
    stockplot = pd.concat([norm_prices_df[ticker], norm_prices_df['SPY'], rs_ratio1[f'{ticker}_rs_ratio'], rs_momentum1[f'{ticker}_rm_ratio']], axis=1)
    
    # Plot ticker and SPY together in one subplot, and RS-Ratio and RS-Momentum in separate subplots
    fig, axes = plt.subplots(3, 1,
                             figsize=(10, 8))  # Create 3 subplots (1 for AMD/SPY and 2 for RS-Ratio and RS-Momentum)
    
    # Plot AMD and SPY in the first subplot
    stockplot[[ticker, 'SPY']].plot(ax=axes[0], title=f"{ticker} and SPY Prices")
    axes[0].set_ylabel('Price')
    
    # Plot RS-Ratio in the second subplot
    stockplot[f'{ticker}_rs_ratio'].plot(ax=axes[1], color='green', title=f"{ticker} RS-Ratio")
    axes[1].set_ylabel('RS-Ratio')
    
    # Plot RS-Momentum in the third subplot
    stockplot[f'{ticker}_rm_ratio'].plot(ax=axes[2], color='blue', title=f"{ticker} RS-Momentum")
    axes[2].set_ylabel('RS-Momentum')
    
    # Turn off x-axis labels for subplot 0 and 1
    plt.setp(axes[0].get_xticklabels(), visible=False)
    plt.setp(axes[1].get_xticklabels(), visible=False)
    plt.show()


if __name__ == '__main__':
    main()
    