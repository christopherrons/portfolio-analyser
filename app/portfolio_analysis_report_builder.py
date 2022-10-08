from operator import attrgetter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame

from historical_data import HistoricalData
from model.portfolio_result import PortfolioResult

sns.set()


class PortfolioAnalysisReportBuilder:

    def __init__(self, historical_data: HistoricalData):
        self.historical_data = historical_data

    def build_report(self, report_output_directory: str,
                     current_portfolio_result: PortfolioResult,
                     simulated_portfolio_results: [PortfolioResult],
                     optimization_portfolio_results: [PortfolioResult]):
        sim_max_return: PortfolioResult = max(simulated_portfolio_results, key=attrgetter('annualized_expected_returns'))
        sim_min_std: PortfolioResult = min(simulated_portfolio_results, key=attrgetter('annualized_standard_deviation'))
        sim_matching_std_highest_return: PortfolioResult = self.get_max_return_same_std(current_portfolio_result,
                                                                                        simulated_portfolio_results)
        opt_max_return: PortfolioResult = max(optimization_portfolio_results, key=attrgetter('annualized_expected_returns'))
        opt_min_std: PortfolioResult = min(optimization_portfolio_results, key=attrgetter('annualized_standard_deviation'))
        opt_matching_std_highest_return: PortfolioResult = self.get_max_return_same_std(current_portfolio_result,
                                                                                        optimization_portfolio_results)

        pp = PdfPages(report_output_directory)
        self.add_historical_data(pp)
        pp.savefig(self.create_expected_return_std_plot(optimization_portfolio_results,
                                                        simulated_portfolio_results,
                                                        current_portfolio_result,
                                                        sim_min_std,
                                                        sim_max_return,
                                                        sim_matching_std_highest_return,
                                                        opt_min_std,
                                                        opt_max_return,
                                                        opt_matching_std_highest_return)
                   , bbox_inches='tight')
        pp.savefig(self.add_portfolio_annualized_statistics(current_portfolio_result,
                                                            sim_min_std,
                                                            sim_max_return,
                                                            sim_matching_std_highest_return,
                                                            opt_min_std,
                                                            opt_max_return,
                                                            opt_matching_std_highest_return)
                   , bbox_inches='tight')
        pp.savefig(self.add_portfolio_weight_barplot_portfolio(current_portfolio_result,
                                                               sim_min_std,
                                                               sim_max_return,
                                                               sim_matching_std_highest_return,
                                                               opt_min_std,
                                                               opt_max_return,
                                                               opt_matching_std_highest_return)
                   , bbox_inches='tight')
        pp.savefig(
            self.add_portfolio_weight_barplot_stock(current_portfolio_result,
                                                    sim_min_std,
                                                    sim_max_return,
                                                    sim_matching_std_highest_return,
                                                    opt_min_std,
                                                    opt_max_return,
                                                    opt_matching_std_highest_return),
            bbox_inches='tight')
        pp.savefig(self.add_portfolio_weight_table(current_portfolio_result,
                                                   sim_min_std,
                                                   sim_max_return,
                                                   sim_matching_std_highest_return,
                                                   opt_min_std,
                                                   opt_max_return,
                                                   opt_matching_std_highest_return),
                   bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(current_portfolio_result, 'Current Portfolio Data'), bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(sim_max_return, 'Sim: Max Return Portfolio Data'), bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(sim_min_std, 'Sim: Min Std Portfolio Data'), bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(sim_matching_std_highest_return, 'Sim: Current Std Max Return Portfolio Data'),
                   bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(opt_max_return, 'Opt: Max Return Portfolio Data'), bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(opt_min_std, 'Opt: Min Std Portfolio Data'), bbox_inches='tight')
        pp.savefig(self.add_portfolio_data(opt_matching_std_highest_return, 'Opt: Current Std Max Return Portfolio Data'),
                   bbox_inches='tight')
        pp.close()

    def add_historical_data(self, pp: PdfPages):
        pp.savefig(self.add_mean_to_report(self.historical_data.mean_returns), bbox_inches='tight')
        pp.savefig(self.add_covariance_to_report(self.historical_data.covariance_returns), bbox_inches='tight')

    def add_mean_to_report(self, mean_returns: DataFrame):
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle('Annualized Return Means [%]', fontsize=16)
        sns.barplot(ax=axes, x=mean_returns.index, y=mean_returns.values * 252)
        return fig

    def add_covariance_to_report(self, covariance: DataFrame):
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle('Annualized Return Covariance [%]', fontsize=16)
        sns.heatmap(ax=axes, data=covariance * 252, annot=True)
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
                                   sim_min_std: PortfolioResult,
                                   sim_max_return: PortfolioResult,
                                   sim_matching_std_highest_return: PortfolioResult,
                                   opt_min_std: PortfolioResult,
                                   opt_max_return: PortfolioResult,
                                   opt_matching_std_highest_return: PortfolioResult):
        headers = current_portfolio_result.symbols_in_correct_order
        df = pd.DataFrame(columns=headers,
                          index=["Current", "Sim: Min Std", "Sim: Max Return", "Sim: Current Std Max Return", "Opt: Min Std",
                                 "Opt: Max Return", "Opt: Current Std Max Return"])
        df.loc["Current", :] = current_portfolio_result.get_result_dataframe().iloc[1]
        df.loc["Sim: Min Std", :] = sim_min_std.get_result_dataframe().iloc[1]
        df.loc["Sim: Max Return", :] = sim_max_return.get_result_dataframe().iloc[1]
        df.loc["Sim: Current Std Max Return", :] = sim_matching_std_highest_return.get_result_dataframe().iloc[1]
        df.loc["Opt: Min Std", :] = sim_min_std.get_result_dataframe().iloc[1]
        df.loc["Opt: Max Return", :] = sim_max_return.get_result_dataframe().iloc[1]
        df.loc["Opt: Current Std Max Return", :] = sim_matching_std_highest_return.get_result_dataframe().iloc[1]
        df = df.reset_index(level=0)
        df = df.rename({'index': ''}, axis='columns')
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle("Portfolio Weights [%]", fontsize=25)
        axes.axis('tight')
        axes.axis('off')
        axes.table(cellText=df.values, colLabels=df.columns, loc='center')
        return fig

    def add_portfolio_weight_barplot_stock(self, current_portfolio_result: PortfolioResult,
                                           sim_min_std: PortfolioResult,
                                           sim_max_return: PortfolioResult,
                                           sim_matching_std_highest_return: PortfolioResult,
                                           opt_min_std: PortfolioResult,
                                           opt_max_return: PortfolioResult,
                                           opt_matching_std_highest_return: PortfolioResult):
        headers = current_portfolio_result.symbols_in_correct_order
        df = pd.DataFrame(columns=headers,
                          index=["Current", "Sim: Min Std", "Sim: Max Return", "Sim: Current Std Max Return", "Opt: Min Std",
                                 "Opt: Max Return", "Opt: Current Std Max Return"])
        df.loc["Current", :] = current_portfolio_result.get_result_dataframe().iloc[1]
        df.loc["Sim: Min Std", :] = sim_min_std.get_result_dataframe().iloc[1]
        df.loc["Sim: Max Return", :] = sim_max_return.get_result_dataframe().iloc[1]
        df.loc["Sim: Current Std Max Return", :] = sim_matching_std_highest_return.get_result_dataframe().iloc[1]
        df.loc["Opt: Min Std", :] = opt_min_std.get_result_dataframe().iloc[1]
        df.loc["Opt: Max Return", :] = opt_max_return.get_result_dataframe().iloc[1]
        df.loc["Opt: Current Std Max Return", :] = opt_matching_std_highest_return.get_result_dataframe().iloc[1]
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle('Portfolio Weight Bar Chart - Stocks', fontsize=16)
        df.T.plot.bar(ax=axes)
        plt.ylabel("Weight [%]")
        return fig

    def add_portfolio_weight_barplot_portfolio(self, current_portfolio_result: PortfolioResult,
                                               sim_min_std: PortfolioResult,
                                               sim_max_return: PortfolioResult,
                                               sim_matching_std_highest_return: PortfolioResult,
                                               opt_min_std: PortfolioResult,
                                               opt_max_return: PortfolioResult,
                                               opt_matching_std_highest_return: PortfolioResult):
        headers = current_portfolio_result.symbols_in_correct_order
        df = pd.DataFrame(columns=headers,
                          index=["Current", "Sim: Min Std", "Sim: Max Return", "Sim: Current Std Max Return", "Opt: Min Std",
                                 "Opt: Max Return", "Opt: Current Std Max Return"])
        df.loc["Current", :] = current_portfolio_result.get_result_dataframe().iloc[1]
        df.loc["Sim: Min Std", :] = sim_min_std.get_result_dataframe().iloc[1]
        df.loc["Sim: Max Return", :] = sim_max_return.get_result_dataframe().iloc[1]
        df.loc["Sim: Current Std Max Return", :] = sim_matching_std_highest_return.get_result_dataframe().iloc[1]
        df.loc["Opt: Min Std", :] = opt_min_std.get_result_dataframe().iloc[1]
        df.loc["Opt: Max Return", :] = opt_max_return.get_result_dataframe().iloc[1]
        df.loc["Opt: Current Std Max Return", :] = opt_matching_std_highest_return.get_result_dataframe().iloc[1]
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle('Portfolio Weight Bar Chart - Portfolio', fontsize=16)
        df.plot.bar(ax=axes)
        plt.ylabel("Weight [%]")
        return fig

    def add_portfolio_annualized_statistics(self, current_portfolio_result: PortfolioResult,
                                            sim_min_std: PortfolioResult,
                                            sim_max_return: PortfolioResult,
                                            sim_matching_std_highest_return: PortfolioResult,
                                            opt_min_std: PortfolioResult,
                                            opt_max_return: PortfolioResult,
                                            opt_matching_std_highest_return: PortfolioResult):
        headers = ["Expected Return %", "Variance", "Standard Deviation"]
        df = pd.DataFrame(columns=headers,
                          index=["Current", "Sim: Min Std", "Sim: Max Return", "Sim: Current Std Max Return", "Opt: Min Std",
                                 "Opt: Max Return", "Opt: Current Std Max Return"])
        df.loc["Current", :] = current_portfolio_result.get_result_statistics_dataframe().iloc[0]
        df.loc["Sim: Min Std", :] = sim_min_std.get_result_statistics_dataframe().iloc[0]
        df.loc["Sim: Max Return", :] = sim_max_return.get_result_statistics_dataframe().iloc[0]
        df.loc["Sim: Current Std Max Return", :] = sim_matching_std_highest_return.get_result_statistics_dataframe().iloc[0]
        df.loc["Opt: Min Std", :] = opt_min_std.get_result_statistics_dataframe().iloc[0]
        df.loc["Opt: Max Return", :] = opt_max_return.get_result_statistics_dataframe().iloc[0]
        df.loc["Opt: Current Std Max Return", :] = opt_matching_std_highest_return.get_result_statistics_dataframe().iloc[0]
        df = df.T
        df = df.reset_index(level=0)
        df = df.rename({'index': ''}, axis='columns')
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle("Annualized Return Statistics ", fontsize=16)
        axes.axis('tight')
        axes.axis('off')
        axes.table(cellText=df.values, colLabels=df.columns, loc='center')
        return fig

    def create_expected_return_std_plot(self, optimization_portfolio_results: [PortfolioResult],
                                        simulated_portfolio_results: [PortfolioResult],
                                        current_portfolio: PortfolioResult,
                                        sim_min_std: PortfolioResult,
                                        sim_max_return: PortfolioResult,
                                        sim_matching_std_highest_return: PortfolioResult,
                                        opt_min_std: PortfolioResult,
                                        opt_max_return: PortfolioResult,
                                        opt_matching_std_highest_return: PortfolioResult):
        fig, axes = plt.subplots(1, figsize=(12, 4))
        fig.suptitle("Annualized Expected Return Vs Std", fontsize=16)
        axes.scatter(y=[r.annualized_expected_returns for r in simulated_portfolio_results],
                     x=[r.annualized_standard_deviation for r in simulated_portfolio_results], label="simulated", c="blue", s=2,
                     alpha=[.90 * abs(r.annualized_expected_returns / sim_max_return.annualized_expected_returns) for r in
                            simulated_portfolio_results])
        axes.scatter(y=[r.annualized_expected_returns for r in optimization_portfolio_results],
                     x=[r.annualized_standard_deviation for r in optimization_portfolio_results], label="opt: efficient-frontier", c="black", s=2,
                     alpha=0.95)
        axes.scatter(y=current_portfolio.annualized_expected_returns,
                     x=current_portfolio.annualized_standard_deviation, label="current", c="red", alpha=0.9, s=100)
        axes.scatter(y=sim_min_std.annualized_expected_returns,
                     x=sim_min_std.annualized_standard_deviation, label="sim: min-std", c="green", alpha=0.9, s=100)
        axes.scatter(y=sim_max_return.annualized_expected_returns,
                     x=sim_max_return.annualized_standard_deviation, label="sim: max-return", c="purple", alpha=0.9, s=100)
        axes.scatter(y=sim_matching_std_highest_return.annualized_expected_returns,
                     x=sim_matching_std_highest_return.annualized_standard_deviation, label="sim: max-return-current-std", c="pink",
                     alpha=0.9, s=100)
        axes.scatter(y=opt_min_std.annualized_expected_returns,
                     x=opt_min_std.annualized_standard_deviation, label="opt: min-std", c="orange", alpha=0.9, s=100)
        axes.scatter(y=opt_max_return.annualized_expected_returns,
                     x=opt_max_return.annualized_standard_deviation, label="opt: max-return", c="brown", alpha=0.9, s=100)
        axes.scatter(y=opt_matching_std_highest_return.annualized_expected_returns,
                     x=opt_matching_std_highest_return.annualized_standard_deviation, label="opt: max-return-current-std", c="aqua",
                     alpha=0.9, s=100)
        axes.scatter(y=[mean * 252 for mean in self.historical_data.mean_returns.to_numpy()],
                     x=[np.sqrt(self.historical_data.covariance_returns.iloc[idx, idx] * 252)
                        for idx in range(0, len(self.historical_data.mean_returns.to_numpy()))],
                     label="stocks", c="yellow", alpha=0.9,
                     s=50)

        plt.xlabel("Standard Deviation (Volatility)")
        plt.ylabel("Expected Return")
        axes.legend()
        axes.grid(True)
        return fig

    def get_max_return_same_std(self, this_portfolio: PortfolioResult,
                                other_portfolio_results: [PortfolioResult]):
        min_max: PortfolioResult = other_portfolio_results[0]
        max_return = -100
        for result in other_portfolio_results:
            std_diff = abs(result.annualized_standard_deviation - this_portfolio.annualized_standard_deviation)
            if std_diff < 0.0001 and result.annualized_expected_returns > max_return:
                min_max = result
                max_return = result.annualized_expected_returns
        return min_max
