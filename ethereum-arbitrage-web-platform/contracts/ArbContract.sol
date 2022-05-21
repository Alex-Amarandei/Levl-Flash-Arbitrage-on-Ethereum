// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract ArbContract {
    mapping(address => uint256) public userGasAmounts;

    function fundWithGas() public payable {
        uint256 requiredETH = 10000000000000000;
        require(msg.value == requiredETH, "You need to send exactly 0.01 ETH!");

        userGasAmounts[msg.sender] += msg.value;
    }

    function executeOrder(
        address _sender,
        address _token1,
        uint256 _amountToken1,
        address _token2,
        address _exchangeForSelling,
        address _exchangeForBuying
    ) external {}

    function executeFlashSwap() internal {}

    function updateUserGasAmounts(address _user, uint256 _gasUsed) internal {}

    function sendFundsToUser(address payable _user, uint256 _amount) internal {}
}
