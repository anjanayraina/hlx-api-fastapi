from fastapi import APIRouter, Depends, Path
from src.services.blockchain_service import BlockchainService
from src.models.stats import BlockchainStats, TreasuryBalance, AccountBalance, Block, Transaction

router = APIRouter()

def get_blockchain_service():
    return BlockchainService()

@router.get("/stats", response_model=BlockchainStats)
async def get_blockchain_stats(service: BlockchainService = Depends(get_blockchain_service)):
    return service.get_stats()

@router.get("/treasury-balance", response_model=TreasuryBalance)
async def get_treasury_balance(service: BlockchainService = Depends(get_blockchain_service)):
    return service.get_treasury_balance()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

# New Routes Added Below

@router.get("/balance/{address}", response_model=AccountBalance)
async def get_balance(
    address: str = Path(..., title="Wallet Address", description="The public address of the wallet to check."),
    service: BlockchainService = Depends(get_blockchain_service)
):
    """
    Returns the HLX balance for a given wallet address.
    """
    return service.get_account_balance(address)

@router.get("/block/{block_number}", response_model=Block)
async def get_block(
    block_number: int = Path(..., title="Block Number", description="The height of the block to retrieve."),
    service: BlockchainService = Depends(get_blockchain_service)
):
    """
    Retrieves details for a specific block by its number.
    """
    return service.get_block(block_number)

@router.get("/transaction/{tx_hash}", response_model=Transaction)
async def get_transaction(
    tx_hash: str = Path(..., title="Transaction Hash", description="The hash of the transaction to retrieve."),
    service: BlockchainService = Depends(get_blockchain_service)
):
    """
    Retrieves details for a specific transaction by its hash.
    """
    return service.get_transaction(tx_hash)