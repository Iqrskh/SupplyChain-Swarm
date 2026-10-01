// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SupplyChainAudit {

    struct Decision {
        uint256 id;
        string recommendationId;
        string sku;
        string supplier;
        uint256 orderQuantity;
        uint256 estimatedCost;
        string humanDecision;
        string recommendationHash;
        uint256 timestamp;
    }

    uint256 public decisionCount;

    mapping(uint256 => Decision) public decisions;

    event DecisionRecorded(
        uint256 indexed id,
        string recommendationId,
        string sku,
        string supplier,
        string humanDecision,
        uint256 timestamp
    );

    function recordDecision(
        string memory recommendationId,
        string memory sku,
        string memory supplier,
        uint256 orderQuantity,
        uint256 estimatedCost,
        string memory humanDecision,
        string memory recommendationHash
    ) public {

        decisionCount++;

        decisions[decisionCount] = Decision(
            decisionCount,
            recommendationId,
            sku,
            supplier,
            orderQuantity,
            estimatedCost,
            humanDecision,
            recommendationHash,
            block.timestamp
        );

        emit DecisionRecorded(
            decisionCount,
            recommendationId,
            sku,
            supplier,
            humanDecision,
            block.timestamp
        );
    }

    function getDecision(uint256 id)
        public
        view
        returns (Decision memory)
    {
        return decisions[id];
    }
}
