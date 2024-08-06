from dataclasses import dataclass


@dataclass
class AssetBalanceData:

    symbol: str = ""
    free: float = 0
    locked: float = 0

    def __post_init__(self):
        self.total = self.free + self.locked