from solcx import compile_standard, install_solc
import json

install_solc("0.8.20")

with open("blockchain/contracts/SupplyChainAudit.sol", "r") as file:
    contract_source = file.read()

compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SupplyChainAudit.sol": {
                "content": contract_source
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "evm.bytecode"]
                }
            }
        }
    },
    solc_version="0.8.20"
)

with open("blockchain/compiled_contract.json", "w") as file:
    json.dump(compiled, file, indent=2)

print("Smart contract compiled successfully!")
print("Saved to blockchain/compiled_contract.json")
