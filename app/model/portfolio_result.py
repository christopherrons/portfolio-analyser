import numpy as np
import pandas as pd
from pandas import DataFrame

from model.portfolio_result_item import PortfolioResultItem


class PortfolioResult:
    def __init__(self, symbol_to_portfolio_result_item: {str, PortfolioResultItem}, mean_returns: DataFrame, covariance: DataFrame, value: float):
        self.symbol_to_portfolio_result_item: {str, PortfolioResultItem} = symbol_to_portfolio_result_item
        self.symbols_in_correct_order: [str] = mean_returns.index.values.tolist()
        self.weights: np.array = self.build_weight_array()
        self.portfolio_value: float = value
        nr_of_trading_days = 252
        self.annualized_expected_returns: float = self.calculate_expected_return(mean_returns.to_numpy()) * nr_of_trading_days
        self.annualized_variance: float = self.calculate_variance(covariance.to_numpy()) * nr_of_trading_days
        self.annualized_standard_deviation: float = np.sqrt(self.annualized_variance)

    def calculate_expected_return(self, mean_returns: np.array) -> float:
        return mean_returns.dot(self.weights.T)

    def calculate_variance(self, covariance: np.array) -> float:
        return self.weights.dot(covariance).dot(self.weights.T)

    def build_weight_array(self) -> np.array:
        weights = []
        for symbol in self.symbols_in_correct_order:
            weights.append(self.symbol_to_portfolio_result_item[symbol].weight)

        return np.array(weights)

    def get_result_dataframe(self) -> DataFrame:
        index = ["Quantity", "Weight %", "Last Price", "Value"]
        df = pd.DataFrame(columns=self.symbols_in_correct_order + ["Total"], index=index)
        for idx, item in enumerate(self.symbol_to_portfolio_result_item.values()):
            df.loc["Quantity", item.symbol] = round(item.quantity, 3)
            df.loc["Weight %", item.symbol] = round(item.weight * 100, 3)
            df.loc["Last Price", item.symbol] = round(item.last_price, 3)
            df.loc["Value", item.symbol] = round(item.value, 3)
        df.loc["Value", "Total"] = round(df.loc["Value", :].sum(), 3)
        return df.fillna('')

    def get_result_statistics_dataframe(self) -> DataFrame:
        headers = ["Expected Return %", "Variance", "Standard Deviation"]
        df = pd.DataFrame(columns=headers, index=[0])
        df.loc[0, "Expected Return %"] = round(self.annualized_expected_returns * 100, 3)
        df.loc[0, "Variance"] = round(self.annualized_variance, 3)
        df.loc[0, "Standard Deviation"] = round(self.annualized_standard_deviation, 3)
        return df.fillna('')
