// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract ERC20RON is ERC20 {
    constructor(uint256 initialSupply) public ERC20("Leu Romanesc", "RON") {
        _mint(msg.sender, initialSupply);
    }
}
