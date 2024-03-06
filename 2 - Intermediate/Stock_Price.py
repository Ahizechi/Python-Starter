import yfinance as yf
import matplotlib.pyplot as plt

def stock_price(ticker, start_date, end_date, moving_averages=[50, 200], save_plot=False, filename='stock_price.png'):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            raise ValueError('No data found for the given ticker and date range.')

        plt.figure(figsize=(10, 6))
        for ma in moving_averages:
            hist[f'MA{ma}'] = hist['Close'].rolling(window=ma).mean()

        hist[['Close'] + [f'MA{ma}' for ma in moving_averages]].plot()
        plt.title(f'Stock Price of {ticker}')
        plt.xlabel('Date')
        plt.ylabel('Price')

        if save_plot:
            plt.savefig(filename)
        else:
            plt.show()
    except Exception as e:
        print(f'Error: {e}')

# Example usage
# stock_price('AAPL', '2020-01-01', '2021-01-01', moving_averages=[50, 200], save_plot=True, filename='apple_stock.png')
