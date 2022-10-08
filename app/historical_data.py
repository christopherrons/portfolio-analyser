import yfinance as yf
from pandas import DataFrame
from yfinance import Tickers


class HistoricalData:

    def __init__(self, symbols: [str], start_date: str, end_date: str):
        self.tickers: Tickers = yf.Tickers(symbols)
        self.historical_data: DataFrame = yf.download(symbols, start=start_date, end=end_date)
        self.closing_prices: DataFrame = self.historical_data["Close"]
        self.returns: DataFrame = self.calculate_returns()
        self.mean_returns: DataFrame = self.returns.mean()
        self.covariance_returns: DataFrame = self.returns.cov()

    def calculate_returns(self) -> DataFrame:
        dividends_adjusted_closing_price: DataFrame = self.closing_prices.copy()
        for symbol in self.tickers.symbols:
            symbol_dividends: DataFrame = self.tickers.tickers[symbol].dividends
            for date in symbol_dividends.index:
                if date in dividends_adjusted_closing_price.index:
                    dividends_adjusted_closing_price.loc[date, symbol]: DataFrame = dividends_adjusted_closing_price.loc[date, symbol] - \
                                                                                    symbol_dividends[date]
        return dividends_adjusted_closing_price.pct_change()

    def get_latest_closing_prices(self, symbols: [str]) -> dict:
        symbol_to_value = {}
        for symbol in symbols:
            symbol_to_value[symbol] = self.get_latest_closing_price(symbol)
        return symbol_to_value

    def get_latest_closing_price(self, symbol: str) -> float:
        return self.closing_prices[symbol].iloc[-1]
