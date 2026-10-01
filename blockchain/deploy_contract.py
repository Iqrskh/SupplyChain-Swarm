from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    raise Exception("Could not connect to Ganache")

print("Connected to Ganache")

# Load compiled contract
with open("blockchain/compiled_contract.json", "r") as file:
    compiled = json.load(file)

contract_data = compiled["contracts"]["SupplyChainAudit.sol"]["SupplyChainAudit"]

abi = contract_data["abi"]
bytecode = contract_data["evm"]["bytecode"]["object"]

# Use first Ganache account
account = w3.eth.accounts[0]

print("Deploying from:", account)

# Create contract
SupplyChainAudit = w3.eth.contract(
    abi=abi,
    bytecode=bytecode
)

# Deploy
transaction = SupplyChainAudit.constructor().transact({
    "from": account
})

# Wait for deployment
receipt = w3.eth.wait_for_transaction_receipt(transaction)

contract_address = receipt.contractAddress

print("Smart contract deployed successfully!")
print("Contract address:", contract_address)

# Save deployment information
deployment = {
    "contract_address": contract_address,
    "abi": abi,
    "deployer": account
}

with open("blockchain/deployment.json", "w") as file:
    json.dump(deployment, file, indent=2)

print("Deployment information saved to blockchain/deployment.json")
