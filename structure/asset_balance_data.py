from dataclasses import dataclass


@dataclass
class AssetBalanceData:

    balance: float = 0
    frozen: float = 0

    def __post_init__(self):
        self.available = self.balance - self.frozen