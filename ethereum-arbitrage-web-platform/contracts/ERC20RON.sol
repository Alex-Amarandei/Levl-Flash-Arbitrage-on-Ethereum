// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

/// @title Euro Mock Token
/// @notice Mocks the Euro Token for demonstrating a guaranteed arbitrage opportunity
contract ERC20RON is ERC20 {
    /// @param _initialSupply The initial supply of token (in wei-like format)
    constructor(uint256 _initialSupply) public ERC20("Leu Romanesc", "RON") {
        _mint(msg.sender, _initialSupply);
    }
}
