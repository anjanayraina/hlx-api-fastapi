from web3 import Web3, exceptions
from fastapi import HTTPException
from src.helper.config import config
from typing import Dict, Any


class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(config.rpc_url))
        if config.validator_1_private_key and not config.validator_1_private_key.startswith('0x'):
            self.private_key = "0x" + config.validator_1_private_key
        else:
            self.private_key = config.validator_1_private_key

    def _check_connection(self):
        if not self.w3.is_connected():
            raise HTTPException(status_code=503, detail="Unable to connect to the blockchain node.")

    def get_stats(self) -> Dict[str, Any]:
        # ... (this method remains the same)
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

    def get_account_balance(self, address: str) -> Dict[str, str]:
        # ... (this method remains the same)
        self._check_connection()
        try:
            checksum_address = Web3.to_checksum_address(address)
            balance_wei = self.w3.eth.get_balance(checksum_address)
            return {"address": address, "balance": str(self.w3.from_wei(balance_wei, 'ether'))}
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid address format.")

    def send_transaction(self, to_address: str, value: float) -> Dict[str, str]:
        self._check_connection()
        if not self.private_key or not config.validator_address:
            raise HTTPException(status_code=500, detail="Sender private key or address is not configured.")

        try:
            from_address = Web3.to_checksum_address(config.validator_address)
            to_checksum_address = Web3.to_checksum_address(to_address)

            nonce = self.w3.eth.get_transaction_count(from_address)
            tx = {
                'nonce': nonce,
                'to': to_checksum_address,
                'value': self.w3.to_wei(value, 'ether'),
                'gas': 21000,
                'gasPrice': self.w3.to_wei('10', 'gwei'),
                'chainId': self.w3.eth.chain_id
            }

            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)

            # --- THIS IS THE CORRECTED LINE ---
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

            self.w3.eth.wait_for_transaction_receipt(tx_hash)

            return {"status": "success", "transaction_hash": tx_hash.hex()}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid transaction parameter: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")