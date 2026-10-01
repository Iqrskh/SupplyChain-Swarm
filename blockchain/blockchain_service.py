import json
import hashlib
from web3 import Web3


GANACHE_URL = "http://127.0.0.1:8545"


def connect_blockchain():
    """Connect to the local Ganache blockchain."""
    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

    if not w3.is_connected():
        raise ConnectionError("Could not connect to Ganache.")

    return w3


def load_contract(w3):
    """Load the deployed SupplyChainAudit smart contract."""
    with open("blockchain/deployment.json", "r") as file:
        deployment = json.load(file)

    contract = w3.eth.contract(
        address=deployment["contract_address"],
        abi=deployment["abi"]
    )

    return contract, deployment


def create_recommendation_hash(result):
    """Create SHA-256 hash for the recommendation."""
    data = json.dumps(result, sort_keys=True, default=str)

    return hashlib.sha256(
        data.encode("utf-8")
    ).hexdigest()


def record_decision(
    recommendation_id,
    result,
    human_decision
):
    """Record a human-reviewed decision on blockchain."""

    w3 = connect_blockchain()

    contract, deployment = load_contract(w3)

    account = deployment["deployer"]

    procurement = result.get("procurement", {})

    sku = str(
        result.get("sku")
        or result.get("SKU_ID")
        or result.get("product")
        or "N/A"
    )

    supplier = str(
        procurement.get("supplier")
        or "None"
    )

    order_quantity = int(
        procurement.get("quantity", 0) or 0
    )

    estimated_cost = int(
        float(procurement.get("estimated_cost", 0) or 0)
    )

    recommendation_hash = create_recommendation_hash(result)

    transaction = contract.functions.recordDecision(
        str(recommendation_id),
        sku,
        supplier,
        order_quantity,
        estimated_cost,
        str(human_decision),
        recommendation_hash
    ).transact({
        "from": account
    })

    receipt = w3.eth.wait_for_transaction_receipt(transaction)

    return {
        "transaction_hash": receipt.transactionHash.hex(),
        "contract_address": deployment["contract_address"],
        "recommendation_hash": recommendation_hash,
        "block_number": receipt.blockNumber
    }
