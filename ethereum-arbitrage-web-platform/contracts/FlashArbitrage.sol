// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6;

import "libraries/UniswapV2Library.sol";
import "interfaces/IUniswapV2Router02.sol";
import "interfaces/IUniswapV2Pair.sol";
import "interfaces/IERC20.sol";

uint256 constant MAX_INT = 2**256 - 1;

contract FlashArbitrage {
    address factory;
    IUniswapV2Router02 uniswapRouter;
    IUniswapV2Router02 sushiswapRouter;

    constructor(
        address _factory,
        address _uniswapRouter,
        address _sushiswapRouter
    ) {
        factory = _factory;
        uniswapRouter = IUniswapV2Router02(_uniswapRouter);
        sushiswapRouter = IUniswapV2Router02(_sushiswapRouter);
    }

    receive() external payable {}

    function uniswapV2Call(
        address _sender,
        uint256 _amount0,
        uint256 _amount1,
        bytes calldata _data
    ) external {
        uint256 deadline = block.timestamp + 10;
        address[] memory path = new address[](2);
        uint256 amountToken = _amount0 == 0 ? _amount1 : _amount0;

        address token0 = IUniswapV2Pair(msg.sender).token0();
        address token1 = IUniswapV2Pair(msg.sender).token1();

        require(
            msg.sender == UniswapV2Library.pairFor(factory, token0, token1),
            "Unauthorized"
        );
        require(_amount0 == 0 || _amount1 == 0);

        path[0] = _amount0 == 0 ? token1 : token0;
        path[1] = _amount0 == 0 ? token0 : token1;

        IERC20 token = IERC20(_amount0 == 0 ? token1 : token0);

        token.approve(address(sushiswapRouter), amountToken);

        uint256 amountRequired = UniswapV2Library.getAmountsIn(
            factory,
            amountToken,
            path
        )[0];

        uint256 amountReceived = sushiswapRouter.swapExactTokensForTokens(
            amountToken,
            amountRequired,
            path,
            msg.sender,
            deadline
        )[1];

        require(
            amountReceived > amountRequired,
            "Transaction was not profitable. Reverting..."
        );

        token.transfer(_sender, amountReceived - amountRequired);
    }

    mapping(address => uint256) public userGasAmounts;

    function fundWithGas() public payable {
        uint256 requiredETH = 10000000000000000;
        require(msg.value == requiredETH, "You need to send exactly 0.01 ETH!");

        userGasAmounts[msg.sender] += msg.value;
    }
}
