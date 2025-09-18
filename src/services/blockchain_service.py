from web3 import Web3
from fastapi import HTTPException
from src.helper.config import config


class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(config.rpc_url))

    def get_stats(self):
        if not self.w3.is_connected():
            raise HTTPException(status_code=503, detail="Unable to connect to the blockchain node.")

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

    def get_treasury_balance(self):
        if not config.treasury_address or config.treasury_address == 'YOUR_TREASURY_ADDRESS':
            raise HTTPException(status_code=500, detail="Treasury address is not configured.")

        balance = self.w3.eth.get_balance(Web3.to_checksum_address(config.treasury_address))
        return {"treasuryBalance": str(self.w3.from_wei(balance, 'ether'))}