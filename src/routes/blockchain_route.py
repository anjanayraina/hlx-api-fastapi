from fastapi import APIRouter, Depends, Path, Body
from src.services.blockchain_service import BlockchainService
from src.models.blockchain.stats import (
    BlockchainStats, AccountBalance, SendTransactionRequest, SendTransactionResponse
)

router = APIRouter()

def get_blockchain_service():
    return BlockchainService()

@router.get("/stats", response_model=BlockchainStats)
async def get_blockchain_stats(service: BlockchainService = Depends(get_blockchain_service)):
    return service.get_stats()

@router.get("/balance/{address}", response_model=AccountBalance)
async def get_balance(
    address: str = Path(..., title="Wallet Address"),
    service: BlockchainService = Depends(get_blockchain_service)
):
    return service.get_account_balance(address)

@router.post("/send-transaction", response_model=SendTransactionResponse)
async def send_transaction(
    request: SendTransactionRequest = Body(...),
    service: BlockchainService = Depends(get_blockchain_service)
):
    return service.send_transaction(request.to_address, request.value)