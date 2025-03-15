from web3 import Web3
import os
from src.utils.helpers import log_message, validate_wallet_address, validate_token_amount
from dotenv import load_dotenv

# Load environment variables (e.g., private key, Infura URL)
load_dotenv()

# Connect to Ethereum node (use Infura or Alchemy)
infura_url = os.getenv("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check connection
if web3.isConnected():
    log_message("Connected to Ethereum network")
else:
    log_message("Connection failed", level="error")

# VANGAI token contract details
vangai_address = Web3.toChecksumAddress("YOUR_VANGAI_CONTRACT_ADDRESS")
vangai_abi = [...]  # Add the ABI here

# Create contract instance
vangai_contract = web3.eth.contract(address=vangai_address, abi=vangai_abi)

# Function to check balance
def check_balance(wallet_address):
    balance = vangai_contract.functions.balanceOf(wallet_address).call()
    return web3.fromWei(balance, 'ether')  # Assuming 18 decimals

# Function to send tokens
def send_vangai(sender_private_key, receiver_address, amount):
    """
    Send VANGAI tokens to a specified address.
    """
    # Validate inputs
    validate_wallet_address(receiver_address)
    validate_token_amount(amount)
    
    # Get sender address and nonce
    sender_address = web3.eth.account.privateKeyToAccount(sender_private_key).address
    nonce = web3.eth.getTransactionCount(sender_address)

    # Create transaction
    txn = vangai_contract.functions.transfer(
        Web3.toChecksumAddress(receiver_address),
        web3.toWei(amount, 'ether')
    ).buildTransaction({
        'chainId': 1,  # Mainnet
        'gas': 200000,
        'gasPrice': web3.toWei('50', 'gwei'),
        'nonce': nonce,
    })

    # Sign and send transaction
    signed_txn = web3.eth.account.signTransaction(txn, private_key=sender_private_key)
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(txn_hash)

