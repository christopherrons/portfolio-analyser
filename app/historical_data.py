import yfinance as yf
from pandas import DataFrame


class HistoricalData:

    def __init__(self, symbols: [str], start_date: str, end_date: str):
        self.historical_data: DataFrame = yf.download(symbols, start=start_date, end=end_date)
        self.closing_prices: DataFrame = self.historical_data["Close"]
        # dividends = historical_data["Dividends"]
        self.returns: DataFrame = self.closing_prices.pct_change()
        self.mean_returns: DataFrame = self.returns.mean()
        self.covariance: DataFrame = self.returns.cov()

    def get_latest_closing_prices(self, symbols: [str]) -> dict:
        symbol_to_value = {}
        for symbol in symbols:
            symbol_to_value[symbol] = self.get_latest_closing_price(symbol)
        return symbol_to_value

    def get_latest_closing_price(self, symbol: str) -> float:
        return self.closing_prices[symbol].iloc[-1]
