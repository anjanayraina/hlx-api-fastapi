from web3 import Web3, exceptions
from fastapi import HTTPException
from src.helper.config import config
from typing import Dict, Any


class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(config.rpc_url))

    def _check_connection(self):
        if not self.w3.is_connected():
            raise HTTPException(status_code=503, detail="Unable to connect to the blockchain node.")

    def get_stats(self) -> Dict[str, Any]:
        self._check_connection()
        block_number = self.w3.eth.block_number
        validator_balance = self.w3.eth.get_balance(Web3.to_checksum_address(config.validator_address))
        burn_balance = self.w3.eth.get_balance(Web3.to_checksum_address(config.burn_address))
        chain_id = self.w3.eth.chain_id

        return {
            "blockNumber": block_number,
            "validatorBalance": str(self.w3.from_wei(validator_balance, 'ether')),
            "burnBalance": str(self.w3.from_wei(burn_balance, 'ether')),
            "isConnected": True,
            "chainId": chain_id
        }

    def get_treasury_balance(self) -> Dict[str, str]:
        self._check_connection()
        if not config.treasury_address or config.treasury_address == 'YOUR_TREASURY_ADDRESS':
            raise HTTPException(status_code=500, detail="Treasury address is not configured.")

        balance = self.w3.eth.get_balance(Web3.to_checksum_address(config.treasury_address))
        return {"treasuryBalance": str(self.w3.from_wei(balance, 'ether'))}

    # New Methods Added Below

    def get_account_balance(self, address: str) -> Dict[str, str]:
        self._check_connection()
        try:
            checksum_address = Web3.to_checksum_address(address)
            balance_wei = self.w3.eth.get_balance(checksum_address)
            return {
                "address": address,
                "balance": str(self.w3.from_wei(balance_wei, 'ether'))
            }
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid address format.")

    def get_block(self, block_number: int) -> Dict[str, Any]:
        self._check_connection()
        try:
            block_data = self.w3.eth.get_block(block_number)
            return {
                "number": block_data['number'],
                "hash": block_data['hash'].hex(),
                "parentHash": block_data['parentHash'].hex(),
                "timestamp": block_data['timestamp'],
                "transactions": [tx.hex() for tx in block_data['transactions']]
            }
        except exceptions.BlockNotFound:
            raise HTTPException(status_code=404, detail=f"Block {block_number} not found.")

    def get_transaction(self, tx_hash: str) -> Dict[str, Any]:
        self._check_connection()
        try:
            tx_data = self.w3.eth.get_transaction(tx_hash)
            return {
                "hash": tx_data['hash'].hex(),
                "blockNumber": tx_data['blockNumber'],
                "from_address": tx_data['from'],
                "to_address": tx_data['to'],
                "value": str(self.w3.from_wei(tx_data['value'], 'ether')),
                "gas": tx_data['gas'],
                "gasPrice": str(self.w3.from_wei(tx_data['gasPrice'], 'gwei')) + " Gwei"
            }
        except exceptions.TransactionNotFound:
            raise HTTPException(status_code=404, detail=f"Transaction {tx_hash} not found.")