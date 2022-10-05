class Position:
    def __init__(self, symbol: str, quantity: float, latest_price: float):
        self.symbol = symbol
        self.quantity = quantity
        self.latest_price = latest_price
        self.value = latest_price * quantity
