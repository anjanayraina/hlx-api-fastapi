from pydantic import BaseModel

class BlockchainStats(BaseModel):
    blockNumber: int
    validatorBalance: str
    burnBalance: str
    isConnected: bool
    chainId: int

class TreasuryBalance(BaseModel):
    treasuryBalance: str