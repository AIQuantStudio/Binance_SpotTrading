from dataclasses import dataclass


@dataclass
class AssetBalanceData:

    currency: str = ""
    free: float = 0
    locked: float = 0

    def __post_init__(self):
        self.total = self.free + self.locked
        

@dataclass
class BianceAccountData:

    name: str
    id: str
    api_key: str
    secret_key: str



@dataclass
class BianceTestAccountData:

    name: str
    id: str
    db: str
