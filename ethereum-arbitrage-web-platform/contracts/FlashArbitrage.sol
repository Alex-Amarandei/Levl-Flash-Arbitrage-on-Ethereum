// SPDX-License-Identifier: MIT

pragma solidity =0.6.6;

import "../libraries/UniswapV2Library.sol";
import "../interfaces/IERC20.sol";
import "../interfaces/IUniswapV2Pair.sol";
import "../interfaces/IUniswapV2Callee.sol";
import "../interfaces/IUniswapV2Router02.sol";
import "../libraries/FullMath.sol";

/// @title Flash Arbitrage Contract
/// @author Amarandei Matei Alexandru (@Alex-Amarandei)
/// @notice Performs a Flash Swap composed of Flash Loan on Sushiswap, Swap on Uniswap
/**
 * @dev Implements the IUniswapV2Callee interface
 * in order to be called by the subsiding pair contract
 */
contract FlashArbitrage is IUniswapV2Callee {
    IUniswapV2Router02 immutable uniswapRouter;

    /// @param The address of the Uniswap V2 Router Contract
    constructor(address _uniswapRouter) public {
        uniswapRouter = IUniswapV2Router02(_uniswapRouter);
    }

    /// @param _owner The Arbitrage Platform's wallet address
    /// @param _amountToken0 The amount of token 0 to be swapped
    /// @param _amountToken1 The amount of token 1 to be swapped
    /// @dev One of the amounts will always be 0 to trigger the flash loan
    /**
     * @param _data Encodes the amount to be repaid to the Sushiswap contract,
     * the deadline (UNIX Timestamp) before the transaction is cancelled
     * and the address of the user who placed the order
     */
    /**
     * @notice Is called by the pair in which the swap occurs and transfers:
     * - the tax to the platform's wallet
     * - the profits to the user who placed the order
     */
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

    /// @param _amountInToken The amount to be sold of the token provided
    /// @param _inTokenAddress The address of the token to be sold
    /// @param _outTokenAddress The address of the token to be bought
    /// @param _amountToRepay The amount to be repaid to the Sushiswap contract
    /// @param _deadline The deadline (UNIX Timestamp) before the transaction is cancelled
    /// @return The IERC20 Token that was bought and the profit made
    /**
     * @notice Is called by the uniswapV2Call function and:
     * - executes the optimistic swap
     * - transfers the amount borrowed to the Sushiswap contract
     */
    function executeSwap(
        uint256 _amountInToken,
        address _inTokenAddress,
        address _outTokenAddress,
        uint256 _amountToRepay,
        uint256 _deadline
    ) internal returns (IERC20, uint256) {
        IERC20 outToken = IERC20(_outTokenAddress);
        uint256 amountGained;

        IERC20(_inTokenAddress).approve(address(uniswapRouter), _amountInToken);

        {
            address[] memory path = new address[](2);
            path[0] = _inTokenAddress;
            path[1] = _outTokenAddress;

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
