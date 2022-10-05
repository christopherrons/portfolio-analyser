import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame

from historical_data import HistoricalData
from model.portfolio_result import PortfolioResult

from operator import attrgetter
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


class PortfolioAnalysisReportBuilder:

    def build_report(self, report_output_directory: str,
                     current_portfolio_result: PortfolioResult,
                     simulated_portfolio_results: [PortfolioResult],
                     optimization_portfolio_results: [PortfolioResult],
                     historical_date: HistoricalData):
        max_return: PortfolioResult = max(simulated_portfolio_results, key=attrgetter('annualized_expected_returns'))
        min_variance: PortfolioResult = min(simulated_portfolio_results, key=attrgetter('annualized_variance'))
        matching_variance_highest_return: PortfolioResult = self.get_max_return_same_variance(current_portfolio_result, simulated_portfolio_results)

        pp = PdfPages(report_output_directory)
        self.add_historical_data(pp, historical_date)
        pp.savefig(self.create_expected_return_variane_plot(simulated_portfolio_results, current_portfolio_result, min_variance, max_return,
                                                            matching_variance_highest_return), bbox_inches='tight')
        pp.savefig(self.add_portfolio_annualized_statistics(current_portfolio_result, min_variance, max_return, matching_variance_highest_return),
                   bbox_inches='tight')
        pp.savefig(self.add_portfolio_weight_barplot_portfolio(current_portfolio_result, min_variance, max_return, matching_variance_highest_return),
                   bbox_inches='tight')
        pp.savefig(self.add_portfolio_weight_barplot_stock(current_portfolio_result, min_variance, max_return, matching_variance_highest_return),
                   bbox_inches='tight')
        pp.savefig(self.add_portfolio_weight_table(current_portfolio_result, min_variance, max_return, matching_variance_highest_return),
                   bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(current_portfolio_result, 'Current Portfolio Data'), bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(max_return, 'Sim: Max Return Portfolio Data'), bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(min_variance, 'Sim: Min Variance Portfolio Data'), bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(matching_variance_highest_return, 'Sim: Current Variance Max Return Portfolio Data'), bbox_inches='tight')

        #  pp.savefig(self.add_weight_bar_chart(current_portfolio_result, min_variance, max_return), bbox_inches='tight')
        pp.close()
        # Bars of weights for current and min variance and max return
        # Table Expected returd for current, min variance and max return
        # Plot of all results with current, min variane and max return in the legend

    def add_historical_data(self, pp: PdfPages, historical_date: HistoricalData):
        pp.savefig(self.add_mean_to_report(historical_date.mean_returns), bbox_inches='tight')
        pp.savefig(self.add_covariance_to_report(historical_date.covariance_returns), bbox_inches='tight')

    def add_mean_to_report(self, mean_returns: DataFrame):
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle('Return Means', fontsize=16)
        sns.barplot(ax=axes, x=mean_returns.index, y=mean_returns.values)
        return fig

    def add_covariance_to_report(self, covariance: DataFrame):
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle('Return Covariance', fontsize=16)
        sns.heatmap(ax=axes, data=covariance, annot=True)
        return fig

    def add_portfolio_data(self, current_portfolio_result: PortfolioResult, title: str):
        df = current_portfolio_result.get_result_dataframe()
        df = df.reset_index(level=0)
        df = df.rename({'index': ''}, axis='columns')
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle(title, fontsize=16)
        axes.axis('tight')
        axes.axis('off')
        axes.table(cellText=df.values, colLabels=df.columns, loc='center')
        return fig

    def add_portfolio_weight_table(self, current_portfolio_result: PortfolioResult,
                                   min_variance: PortfolioResult,
                                   max_return: PortfolioResult,
                                   matching_variance_highest_return: PortfolioResult):
        headers = current_portfolio_result.symbols_in_correct_order
        df = pd.DataFrame(columns=headers, index=["Current", "Min Variance", "Max Return", "Current Variance Max Return"])
        df.loc["Current", :] = current_portfolio_result.get_result_dataframe().iloc[1]
        df.loc["Min Variance", :] = min_variance.get_result_dataframe().iloc[1]
        df.loc["Max Return", :] = max_return.get_result_dataframe().iloc[1]
        df.loc["Current Variance Max Return", :] = matching_variance_highest_return.get_result_dataframe().iloc[1]
        df = df.reset_index(level=0)
        df = df.rename({'index': ''}, axis='columns')
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle("Portfolio Weights", fontsize=25)
        axes.axis('tight')
        axes.axis('off')
        axes.table(cellText=df.values, colLabels=df.columns, loc='center')
        return fig

    def add_portfolio_weight_barplot_stock(self, current_portfolio_result: PortfolioResult,
                                           min_variance: PortfolioResult,
                                           max_return: PortfolioResult,
                                           matching_variance_highest_return: PortfolioResult):
        headers = current_portfolio_result.symbols_in_correct_order
        df = pd.DataFrame(columns=headers, index=["Current", "Sim: Min Variance", "Sim: Max Return", "Sim: Current Variance Max Return"])
        df.loc["Current", :] = current_portfolio_result.get_result_dataframe().iloc[1]
        df.loc["Sim: Min Variance", :] = min_variance.get_result_dataframe().iloc[1]
        df.loc["Sim: Max Return", :] = max_return.get_result_dataframe().iloc[1]
        df.loc["Sim: Current Variance Max Return", :] = matching_variance_highest_return.get_result_dataframe().iloc[1]

        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle('Portfolio Weight Bar Chart - Stocks', fontsize=16)
        df.T.plot.bar(ax=axes)
        return fig

    def add_portfolio_weight_barplot_portfolio(self, current_portfolio_result: PortfolioResult,
                                               min_variance: PortfolioResult,
                                               max_return: PortfolioResult,
                                               matching_variance_highest_return: PortfolioResult):
        headers = current_portfolio_result.symbols_in_correct_order
        df = pd.DataFrame(columns=headers, index=["Current", "Sim: Min Variance", "Sim: Max Return", "Sim: Current Variance Max Return"])
        df.loc["Current", :] = current_portfolio_result.get_result_dataframe().iloc[1]
        df.loc["Sim: Min Variance", :] = min_variance.get_result_dataframe().iloc[1]
        df.loc["Sim: Max Return", :] = max_return.get_result_dataframe().iloc[1]
        df.loc["Sim: Current Variance Max Return", :] = matching_variance_highest_return.get_result_dataframe().iloc[1]

        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle('Portfolio Weight Bar Chart - Portfolio', fontsize=16)
        df.plot.bar(ax=axes)
        return fig

    def add_portfolio_annualized_statistics(self, current_portfolio_result: PortfolioResult,
                                            min_variance: PortfolioResult,
                                            max_return: PortfolioResult,
                                            matching_variance_highest_return: PortfolioResult):
        headers = ["Expected Return %", "Variance", "Standard Deviation"]
        df = pd.DataFrame(columns=headers, index=["Current", "Sim: Min Variance", "Sim: Max Return", "Sim: Current Variance Max Return"])
        df.loc["Current", :] = current_portfolio_result.get_result_statistics_dataframe().iloc[0]
        df.loc["Sim: Min Variance", :] = min_variance.get_result_statistics_dataframe().iloc[0]
        df.loc["Sim: Max Return", :] = max_return.get_result_statistics_dataframe().iloc[0]
        df.loc["Sim: Current Variance Max Return", :] = matching_variance_highest_return.get_result_statistics_dataframe().iloc[0]
        df = df.reset_index(level=0)
        df = df.rename({'index': ''}, axis='columns')
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle("Annualized Return Statistics ", fontsize=16)
        axes.axis('tight')
        axes.axis('off')
        axes.table(cellText=df.values, colLabels=df.columns, loc='center')
        return fig

    def create_expected_return_variane_plot(self, simulated_portfolio_results: [PortfolioResult],
                                            current_portfolio: PortfolioResult,
                                            min_variance: PortfolioResult,
                                            max_return: PortfolioResult,
                                            matching_variance_highest_return: PortfolioResult):
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle("Expected Return Vs Variance", fontsize=16)
        axes.scatter(y=[r.annualized_expected_returns for r in simulated_portfolio_results],
                     x=[r.annualized_variance for r in simulated_portfolio_results], label="simulated", c="blue", s=2,
                     alpha=[.90 * abs(r.annualized_expected_returns / max_return.annualized_expected_returns) for r in simulated_portfolio_results])
        axes.scatter(y=current_portfolio.annualized_expected_returns,
                     x=current_portfolio.annualized_variance, label="current", c="red", alpha=0.9, s=100)
        axes.scatter(y=min_variance.annualized_expected_returns,
                     x=min_variance.annualized_variance, label="sim: min-variance", c="green", alpha=0.9, s=100)
        axes.scatter(y=max_return.annualized_expected_returns,
                     x=max_return.annualized_variance, label="sim: max-return", c="purple", alpha=0.9, s=100)
        axes.scatter(y=matching_variance_highest_return.annualized_expected_returns,
                     x=matching_variance_highest_return.annualized_variance, label="sim: max-return-current-variance", c="pink", alpha=0.9, s=100)

        axes.legend()
        axes.grid(True)
        return fig

    def get_max_return_same_variance(self, current_portfolio: PortfolioResult,
                                     simulated_portfolio_results: [PortfolioResult]):
        min_max: PortfolioResult = simulated_portfolio_results[0]
        max_return = -100
        for result in simulated_portfolio_results:
            variance_diff = abs(result.annualized_variance - current_portfolio.annualized_variance)
            if variance_diff < 0.0001 and result.annualized_expected_returns > max_return:
                min_max = result
                max_return = result.annualized_expected_returns
        return min_max
