from pydantic import BaseModel
from typing import List, Optional

class BlockchainStats(BaseModel):
    blockNumber: int
    validatorBalance: str
    burnBalance: str
    isConnected: bool
    chainId: int

class TreasuryBalance(BaseModel):
    treasuryBalance: str


class AccountBalance(BaseModel):
    address: str
    balance: str

class Transaction(BaseModel):
    hash: str
    blockNumber: Optional[int]
    from_address: str
    to_address: Optional[str]
    value: str
    gas: int
    gasPrice: str

class Block(BaseModel):
    number: int
    hash: str
    parentHash: str
    timestamp: int
    transactions: List[str]