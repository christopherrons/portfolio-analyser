from typing import List

from position import Position


class Portfolio:

    def __init__(self, symbol_to_position: {str, Position}):
        self.symbol_to_position: {str, Position} = symbol_to_position
        self.value: float = sum(position.value for position in self.symbol_to_position.values())

    def calculate_position_weight(self, symbol: str) -> float:
        return self.symbol_to_position[symbol].value / self.value
