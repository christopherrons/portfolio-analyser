from portfolio_analyser import PortfolioAnalyser
import csv

def main():
    portfolio_analyser: PortfolioAnalyser = PortfolioAnalyser(historical_years=3, positions_file_path="positions.csv")
    portfolio_analyser.create_analysis_report()


if __name__ == "__main__":
    main()
