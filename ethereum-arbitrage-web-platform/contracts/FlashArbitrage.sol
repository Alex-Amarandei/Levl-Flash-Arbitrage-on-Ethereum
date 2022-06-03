// SPDX-License-Identifier: MIT

pragma solidity =0.6.6;

import "../libraries/UniswapV2Library.sol";
import "../interfaces/IERC20.sol";
import "../interfaces/IUniswapV2Pair.sol";
import "../interfaces/IUniswapV2Callee.sol";
import "../interfaces/IUniswapV2Router02.sol";
import "../libraries/FullMath.sol";

contract FlashArbitrage is IUniswapV2Callee {
    IUniswapV2Router02 immutable uniswapRouter;

    constructor(address _uniswapRouter) public {
        uniswapRouter = IUniswapV2Router02(_uniswapRouter);
    }

    function uniswapV2Call(
        address _owner,
        uint256 _amountToken0,
        uint256 _amountToken1,
        bytes calldata _data
    ) external override {
        (uint256 amountToRepay, uint256 deadline, address user) = abi.decode(
            _data,
            (uint256, uint256, address)
        );

        uint256 amount;
        address inTokenAddress;
        address outTokenAddress;

        if (_amountToken0 == 0) {
            amount = _amountToken1;
            inTokenAddress = IUniswapV2Pair(msg.sender).token1();
            outTokenAddress = IUniswapV2Pair(msg.sender).token0();
        } else {
            amount = _amountToken0;
            inTokenAddress = IUniswapV2Pair(msg.sender).token0();
            outTokenAddress = IUniswapV2Pair(msg.sender).token1();
        }

        (IERC20 outToken, uint256 profit) = executeSwap(
            amount,
            inTokenAddress,
            outTokenAddress,
            amountToRepay,
            deadline
        );

        {
            uint256 tax = FullMath.mulDiv(profit, 1, 1000);
            outToken.transfer(payable(_owner), tax);
            profit -= tax;
        }

        outToken.transfer(payable(user), profit);
    }

    function executeSwap(
        uint256 _amountInToken,
        address _inTokenAdress,
        address _outTokenAdress,
        uint256 _amountToRepay,
        uint256 _deadline
    ) internal returns (IERC20, uint256) {
        IERC20 outToken = IERC20(_outTokenAdress);
        uint256 amountGained;

        IERC20(_inTokenAdress).approve(address(uniswapRouter), _amountInToken);

        {
            address[] memory path = new address[](2);
            path[0] = _inTokenAdress;
            path[1] = _outTokenAdress;

            amountGained = uniswapRouter.swapExactTokensForTokens(
                _amountInToken,
                0,
                path,
                address(this),
                _deadline
            )[1];
        }

        outToken.transfer(msg.sender, _amountToRepay);

        return (outToken, amountGained - _amountToRepay);
    }
}
