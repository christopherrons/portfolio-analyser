import csv

import numpy as np

from historical_data import HistoricalData
from model.portfolio import Portfolio
from model.portfolio_result import PortfolioResult
from model.portfolio_result_item import PortfolioResultItem
from model.position import Position
from portfolio_analysis_report_builder import PortfolioAnalysisReportBuilder
from utils.utils import Utils


class PortfolioAnalyser:
    def __init__(self, historical_years: int, positions_file_path: str):
        self.symbols: [str] = self.get_symbols_from_csv(positions_file_path)
        self.historical_data: HistoricalData = HistoricalData(
            symbols=self.symbols,
            start_date=Utils.get_date_string_today_n_years_back(historical_years),
            end_date=Utils.get_date_string_yesterday(),
        )
        symbol_to_position: {str, Position} = self.create_positions_from_csv(positions_file_path)
        self.current_portfolio: Portfolio = Portfolio(symbol_to_position)

    def create_analysis_report(self, report_output_directory: str):
        current_portfolio_result: PortfolioResult = self.create_portfolio_result(self.current_portfolio)
        simulated_portfolio_results: [PortfolioResult] = self.simulate_portfolio_result()
        optimization_portfolio_results: [PortfolioResult] = None  # FIXME: Add this method

        report_builder: PortfolioAnalysisReportBuilder = PortfolioAnalysisReportBuilder()
        report_builder.build_report(report_output_directory, current_portfolio_result, simulated_portfolio_results,
                                    optimization_portfolio_results, self.historical_data)

    def simulate_portfolio_result(self) -> [PortfolioResult]:
        nr_of_simulations = 50000
        portfolio_results: [PortfolioResult] = []
        for simulation in range(0, nr_of_simulations):
            quantities: np.array = np.random.random(len(self.symbols))
            quantities /= sum(quantities)

            symbol_to_positions: {str, Position} = {}

            for index, quantity in enumerate(quantities):
                current_symbol = self.symbols[index]
                symbol_to_positions[current_symbol] = Position(current_symbol, quantity, latest_price=100)

            portfolio_results.append(
                self.create_portfolio_result(Portfolio(symbol_to_positions))
            )
        return portfolio_results

    def create_portfolio_result(self, portfolio: Portfolio) -> PortfolioResult:
        symbol_to_portfolio_result_item: {str, PortfolioResultItem} = {}
        for symbol, position in portfolio.symbol_to_position.items():
            symbol_to_portfolio_result_item[symbol] = PortfolioResultItem(
                symbol,
                portfolio.calculate_position_weight(symbol),
                portfolio.symbol_to_position[symbol].latest_price,
                portfolio.symbol_to_position[symbol].quantity,
                portfolio.symbol_to_position[symbol].value,
            )

        return PortfolioResult(symbol_to_portfolio_result_item,
                               self.historical_data.mean_returns,
                               self.historical_data.covariance_returns,
                               portfolio.value)

    def create_positions_from_csv(self, positions_file_path: str) -> {str, Position}:
        symbol_to_positions: {str, Position} = {}
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

    def get_symbols_from_csv(self, positions_file_path: str) -> [str]:
        symbols: [str] = []
        with open(positions_file_path) as file:
            type(file)
            csvreader = csv.reader(file)
            next(csvreader)
            for position in csvreader:
                symbols.append(position[0].strip())

        return symbols
