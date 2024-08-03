from dataclasses import dataclass

from structure.enumeration import Direction, Offset

@dataclass
class TradeData:
    """"""
    symbol: str
    order_id: str
    trade_id: str
    direction: Direction = None

    offset: Offset = Offset.NONE
    price: float = 0
    volume: float = 0
    datetime = None

    def __post_init__(self):
        """"""
        # self.vt_symbol = f"{self.symbol}.{self.exchange.value}"
        # self.vt_order_id = f"{self.gateway_name}.{self.order_id}"
        # self.vt_trade_id = f"{self.gateway_name}.{self.trade_id}"
        pass