# Portfolio Analyser

The application does analysis of a stock portfolio based on historical market data from [yahoo finance](https://finance.yahoo.com) and `Modern
Portfolio Theory`. The goal is to find the minium variance portfolio based on historical returns. This is done by simulating the weights of the
portfolio and is also done by solving a constraint quadratic optimization problem. The results are the aggregated to a report to serve as a means of
analysis of the portfolio.

## How to Run the Application

1. Install relevant packages `pip install -r requirements.txt`
2. Run `python main.py --help` to see input options.
3. Add symbols and quantity to a csv file.
    * The ticker symbol has to match [yahoo finance](https://finance.yahoo.com).
    * The CSV has the header `Symbol | Quantity` where the quantity can be set to 0 if no stocks are owned.
4. Run the program again with/without args to generata a report,
   see [analysis_report_from_2019-10-09_to_2022-10-08.pdf](analysis_report_from_2019-10-09_to_2022-10-08.pdf) for expected output.
