// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract RONZero is ERC20 {
    constructor(uint256 initialSupply) public ERC20("Leu Romanesc", "RONZero") {
        _mint(msg.sender, initialSupply);
    }
}
