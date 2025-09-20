import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        env_path = os.path.join(os.path.dirname(__file__), '..', 'resources', '.env.dev')
        load_dotenv(dotenv_path=env_path)
        self.rpc_url = os.getenv("RPC_URL")
        self.validator_address = os.getenv("VALIDATOR_ADDRESS")
        self.burn_address = os.getenv("BURN_ADDRESS")
        self.validator_1_private_key = os.getenv("VALIDATOR_1_PRIVATE_KEY")


config = Config()