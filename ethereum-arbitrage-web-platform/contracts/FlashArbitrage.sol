// SPDX-License-Identifier: MIT

pragma solidity =0.6.6;

import "libraries/UniswapV2Library.sol";
import "interfaces/IERC20.sol";
import "interfaces/IUniswapV2Pair.sol";
import "interfaces/IUniswapV2Callee.sol";
import "interfaces/IUniswapV2Router02.sol";

contract FlashArbitrage is IUniswapV2Callee {
    address immutable sFactory;
    IUniswapV2Router02 immutable uRouter;

    constructor(address _sFactory, address _uRouter) public {
        sFactory = _sFactory;
        uRouter = IUniswapV2Router02(_uRouter);
    }

    function uniswapV2Call(
        address _sender,
        uint256 _amount0,
        uint256 _amount1,
        bytes calldata _data
    ) external override {
        address[] memory path = new address[](2);
        (uint256 amountRequired, uint256 deadline) = abi.decode(
            _data,
            (uint256, uint256)
        );
        if (_amount0 == 0) {
            uint256 amountEntryToken = _amount1;
            address token0 = IUniswapV2Pair(msg.sender).token0();
            address token1 = IUniswapV2Pair(msg.sender).token1();
            IERC20 entryToken = IERC20(token1);
            IERC20 exitToken = IERC20(token0);
            entryToken.approve(address(uRouter), amountEntryToken);
            path[0] = token1;
            path[1] = token0;
            uint256 amountReceived = uRouter.swapExactTokensForTokens(
                amountEntryToken,
                0,
                path,
                address(this),
                deadline
            )[1];
            exitToken.transfer(msg.sender, amountRequired);
            exitToken.transfer(_sender, amountReceived - amountRequired);
        } else {
            uint256 amountEntryToken = _amount0;
            address token0 = IUniswapV2Pair(msg.sender).token0();
            address token1 = IUniswapV2Pair(msg.sender).token1();
            IERC20 entryToken = IERC20(token0);
            IERC20 exitToken = IERC20(token1);
            entryToken.approve(address(uRouter), amountEntryToken);
            path[0] = token0;
            path[1] = token1;
            uint256 amountReceived = uRouter.swapExactTokensForTokens(
                amountEntryToken,
                0,
                path,
                address(this),
                deadline
            )[1];
            exitToken.transfer(msg.sender, amountRequired);
            exitToken.transfer(_sender, amountReceived - amountRequired);
        }
    }

    mapping(address => uint256) public userGasAmounts;

    function fundWithGas() public payable {
        uint256 requiredETH = 10000000000000000;
        require(msg.value == requiredETH, "You need to send exactly 0.01 ETH!");

        userGasAmounts[msg.sender] += msg.value;
    }
}
