import csv

from historical_data import HistoricalData
from portfolio import Portfolio
from portfolio_result import PortfolioResult
from portfolio_result_item import PortfolioResultItem
from position import Position

from utils import Utils


class PortfolioAnalyser:
    def __init__(self, historical_years: int, positions_file_path: str):
        symbol_to_position = self.create_positions(positions_file_path)
        self.current_portfolio: Portfolio = Portfolio(symbol_to_position)
        self.historical_data: HistoricalData = HistoricalData(
            symbols=list(symbol_to_position.keys()),
            start_date=Utils.get_date_string_today_n_years_back(historical_years),
            end_date=Utils.get_date_string_yesterday(),
        )

    def create_analysis_report(self):
        a = 1
        pass

    def create_portfolio_result(self) -> PortfolioResult:
        symbol_to_portfolio_result_item = {}
        for symbol, position in self.current_portfolio.symbol_to_positions.items():
            symbol_to_portfolio_result_item[symbol] = PortfolioResultItem(
                symbol,
                self.current_portfolio.calculate_position_weight(symbol),
                self.current_portfolio.symbol_to_positions[symbol].latest_price,
                self.current_portfolio.symbol_to_positions[symbol].quantity,
                self.current_portfolio.symbol_to_positions[symbol].value,
            )

        return PortfolioResult(symbol_to_portfolio_result_item, self.historical_data.mean_returns, self.historical_data.covariance)

    def create_positions(self, positions_file_path: str):
        symbol_to_positions = {}
        with open(positions_file_path) as file:
            type(file)
            csvreader = csv.reader(file)
            next(csvreader)
            for position in csvreader:
                symbol = position[0].strip()
                quantity = float(position[1].strip())
                latest_price = self.historical_data.get_latest_closing_price(symbol)
                symbol_to_positions[symbol] = Position(symbol, quantity, latest_price)

        return symbol_to_positions
