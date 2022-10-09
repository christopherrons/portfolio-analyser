import csv

import numpy as np

from historical_data import HistoricalData
from model.portfolio import Portfolio
from model.portfolio_result import PortfolioResult
from model.portfolio_result_item import PortfolioResultItem
from model.position import Position
from portfolio_analysis_report_builder import PortfolioAnalysisReportBuilder
from quandratic_solver import QuadraticSolver
from utils.utils import Utils


class PortfolioAnalyser:
    def __init__(self, historical_years: int, positions_file_path: str, risk_free_return: float):
        self.symbols: [str] = self.get_symbols_from_csv(positions_file_path)
        self.historical_data: HistoricalData = HistoricalData(
            symbols=self.symbols,
            start_date=Utils.get_date_string_today_n_years_back(historical_years),
            end_date=Utils.get_date_string_yesterday(),
        )
        symbol_to_position: {str, Position} = self.create_positions_from_csv(positions_file_path)
        self.current_portfolio: Portfolio = Portfolio(symbol_to_position)
        self.report_builder: PortfolioAnalysisReportBuilder = PortfolioAnalysisReportBuilder(self.historical_data, risk_free_return)

    def create_analysis_report(self, report_output_directory: str):
        current_portfolio_result: PortfolioResult = self.create_portfolio_result(self.current_portfolio)
        simulated_portfolio_results: [PortfolioResult] = self.simulate_portfolio_result()
        optimization_portfolio_results: [PortfolioResult] = self.optimization_portfolio_result()

        self.report_builder.build_report(report_output_directory, current_portfolio_result, simulated_portfolio_results,
                                         optimization_portfolio_results)

    def optimization_portfolio_result(self) -> [PortfolioResult]:
        print("Calculating Optimized portfolio results...", end=" ")
        mean_returns: np.array = self.historical_data.mean_returns.to_numpy()
        max_mean_returns: float = max(mean_returns)
        min_mean_returns: float = min(mean_returns)
        H: np.array = self.historical_data.correlation_adjusted_covariance.to_numpy()
        A: np.array = np.array([mean_returns, np.ones(len(self.symbols))])
        c: np.array = np.zeros(len(self.symbols))
        c0: np.array = np.zeros(len(self.symbols))
        x0: np.array = np.array([1 / len(self.symbols)] * len(self.symbols))

        portfolio_results: [PortfolioResult] = []
        for expected_return in np.linspace(min_mean_returns, max_mean_returns, 500, endpoint=True):
            b: np.array = np.array([expected_return, 1])
            constraints: [{}] = [{'type': 'eq',
                                  'fun': lambda x: np.dot(A, x) - b,
                                  'jac': lambda x: A}]
            bounds: [()] = [(0, None)] * len(self.symbols)
            result = QuadraticSolver.solve(H, c, c0, x0, constraints, bounds)

            symbol_to_positions: {str, Position} = {}
            for index, quantity in enumerate(result["x"]):
                current_symbol: str = self.historical_data.mean_returns.index.to_numpy()[index]
                symbol_to_positions[current_symbol] = Position(current_symbol, quantity, latest_price=100)
            portfolio_results.append(
                self.create_portfolio_result(Portfolio(symbol_to_positions))
            )
        print("Done!")
        return portfolio_results

    def simulate_portfolio_result(self) -> [PortfolioResult]:
        print("Calculating Simulated portfolio results...", end=" ")
        nr_of_simulations = 50000
        portfolio_results: [PortfolioResult] = []
        for simulation in range(0, nr_of_simulations):
            quantities: np.array = np.random.random(len(self.symbols))
            quantities /= sum(quantities)

            symbol_to_positions: {str, Position} = {}

            for index, quantity in enumerate(quantities):
                current_symbol: str = self.symbols[index]
                symbol_to_positions[current_symbol] = Position(current_symbol, quantity, latest_price=100)

            portfolio_results.append(
                self.create_portfolio_result(Portfolio(symbol_to_positions))
            )
        print("Done!")
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
                               self.historical_data.correlation_adjusted_covariance,
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
