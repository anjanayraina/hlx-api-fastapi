from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from web3 import Web3

# --- Configuration ---
# Your local HLX node's RPC endpoint
RPC_URL = "http://127.0.0.1:8545"
# The validator address to monitor
VALIDATOR_ADDRESS = 'YOUR_VALIDATOR_ADDRESS_WITH_0x'
# The burn address
BURN_ADDRESS = '0x000000000000000000000000000000000000dEaD'

# --- Initialize Application ---
# Create the FastAPI app instance
app = FastAPI(
    title="HLX Blockchain API",
    description="An API to fetch live stats from the custom HLX blockchain node.",
    version="1.0.0"
)

# Add CORS middleware to allow requests from any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create a Web3 provider to connect to the blockchain
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# --- API Endpoint ---
@app.get("/stats")
async def get_blockchain_stats():
    """
    This endpoint connects to the HLX node, fetches key stats,
    and returns them as a JSON object.
    """
    try:
        # 1. Check if the node is connected
        if not w3.is_connected():
            raise HTTPException(status_code=503, detail="Service Unavailable: Unable to connect to the blockchain node.")

        # 2. Fetch data from the blockchain
        block_number = w3.eth.block_number
        validator_wei = w3.eth.get_balance(Web3.to_checksum_address(VALIDATOR_ADDRESS))
        burn_wei = w3.eth.get_balance(Web3.to_checksum_address(BURN_ADDRESS))

        # 3. Format the data and return it. FastAPI handles JSON conversion automatically.
        return {
            "blockNumber": block_number,
            "validatorBalance": str(w3.from_wei(validator_wei, 'ether')), # Convert Decimal to string for JSON
            "burnBalance": str(w3.from_wei(burn_wei, 'ether')),
            "isConnected": True
        }

    except Exception as e:
        # If any other error occurs, raise an HTTPException
        raise HTTPException(status_code=500, detail=str(e))

# --- Health Check Endpoint (Good Practice) ---
@app.get("/health")
async def health_check():
    return {"status": "ok"}