from argparse import ArgumentParser

from portfolio_analyser import PortfolioAnalyser
from utils.utils import Utils


def main():
    arg_parser = ArgumentParser(description='Analysis and Optimization of a Stock Portfolio',
                                epilog='(C) 2022 \nAuthors: Christopher Herron \nEmails: christopherherron09@gmail.com')

    arg_parser.add_argument('--h_year', help='Historical years to look back.', type=int, default=3)
    arg_parser.add_argument('--csv_path', help='Path to positions csv file.', type=str, default="positions.csv")
    arg_parser.add_argument('--report_output_path', help='Output path of the report.', type=str, default="analysis_report")
    args = arg_parser.parse_args()

    portfolio_analyser: PortfolioAnalyser = PortfolioAnalyser(historical_years=args.h_year, positions_file_path=args.csv_path)
    portfolio_analyser.create_analysis_report(
        f"{args.report_output_path}_from_{Utils.get_date_string_today_n_years_back(args.h_year)}_to_{Utils.get_date_string_yesterday()}.pdf")


if __name__ == "__main__":
    main()
