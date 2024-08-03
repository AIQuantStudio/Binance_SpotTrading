from dataclasses import dataclass

from structure.enumeration import Direction, Offset

@dataclass
class BianceAccountData:

    name: str
    id: str
    api_key: str
    secret_key: str
