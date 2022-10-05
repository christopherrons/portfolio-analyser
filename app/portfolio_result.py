import numpy as np
from pandas import DataFrame

from portfolio_result_item import PortfolioResultItem


class PortfolioResult:
    def __init__(self, symbol_to_portfolio_result_item: {str, PortfolioResultItem}, mean_returns: DataFrame, covariance: DataFrame):
        self.symbol_to_portfolio_result_item: {str, PortfolioResultItem} = symbol_to_portfolio_result_item
        self.symbols_in_correct_order = mean_returns.index
        self.mean_returns: np.array = mean_returns.to_numpy()
        self.covariance: np.array = covariance.to_numpy()
        self.weights: np.array = self.build_weight_array()
        self.portfolio_value: float = sum(position.value for position in self.symbol_to_portfolio_result_item.values())
        self.expected_returns: float = self.calculate_expected_return()
        self.variance: float = self.calculate_variance()

    def calculate_expected_return(self) -> float:
        return self.mean_returns.dot(self.weights.T)

    def calculate_variance(self) -> float:
        return self.covariance.dot(self.weights.T).sum()

    def build_weight_array(self) -> np.array:
        weights = []
        for symbol in self.symbols_in_correct_order:
            weights.append(self.symbol_to_portfolio_result_item[symbol].weight)

        return np.array(weights)
