class PortfolioResultItem:

    def __init__(self, symbol: str, weight: float, last_price: float, quantity: float, value: float):
        self.symbol = symbol
        self.weight = weight
        self.last_price = last_price
        self.quantity = quantity
        self.value = value
