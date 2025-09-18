from fastapi import APIRouter, Depends
from src.services.blockchain_service import BlockchainService
from src.models.blockchain.stats import BlockchainStats, TreasuryBalance

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