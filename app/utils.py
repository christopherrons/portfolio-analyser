from datetime import datetime

from dateutil.relativedelta import relativedelta


class Utils:

    @staticmethod
    def get_date_string_yesterday() -> str:
        return (datetime.now() + relativedelta(days=-1)).date().__str__()

    @staticmethod
    def get_date_string_today_n_years_back(historical_years: int) -> str:
        return (datetime.now() + relativedelta(years=-historical_years)).date().__str__()
