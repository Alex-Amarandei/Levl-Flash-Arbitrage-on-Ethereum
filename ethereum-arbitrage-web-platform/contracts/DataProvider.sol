// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";
import "../libraries/Babylonian.sol";
import "../libraries/SafeMath.sol";
import "../libraries/FullMath.sol";

/// @title Data Provider Contract
/// @notice This contract is used by the Flash Arbitrage contract
contract DataProvider {
    using SafeMath for uint256;

    /// @param _priceFeed The address of the ETH/USD price feed
    /// @return ETH price in USD from the Chainlink Oracle
    function getEthPrice(address _priceFeed) public view returns (uint256) {
        (, int256 price, , , ) = AggregatorV3Interface(_priceFeed)
            .latestRoundData();
        return uint256(price * 10000000000);
    }

    /// @notice based on: https://github.com/Uniswap/v2-periphery/blob/master/contracts/libraries/UniswapV2LiquidityMathLibrary.sol
    /// @param _targetReserve0 The intended price of token 0
    /// @param _targetReserve1 The intended price of token 1
    /// @param _currentReserve0 The current price of token 0
    /// @param _currentReserve1 The current price of token 1
    /**
     * @dev The "intended" price represents the price towards which to shift
     * the current price through the use of arbitrage
     */
    /**
     * @return from0To1, amountIn
     * - The direction of the trade
     * - The maximum amount of tokens to be traded
     */
    function getTradeData(
        uint256 _targetReserve0,
        uint256 _targetReserve1,
        uint256 _currentReserve0,
        uint256 _currentReserve1
    ) public pure returns (bool, uint256) {
        bool from0To1 = FullMath.mulDiv(
            _currentReserve0,
            _targetReserve1,
            _currentReserve1
        ) < _targetReserve0;

        uint256 leftSide = Babylonian.sqrt(
            FullMath.mulDiv(
                _currentReserve0.mul(_currentReserve1).mul(1000),
                from0To1 ? _targetReserve0 : _targetReserve1,
                (from0To1 ? _targetReserve1 : _targetReserve0).mul(997)
            )
        );

        uint256 rightSide = (
            from0To1 ? _currentReserve0.mul(1000) : _currentReserve1.mul(1000)
        ) / 997;

        if (leftSide < rightSide) return (false, 0);

        uint256 amountIn = leftSide.sub(rightSide);

        return (from0To1, amountIn);
    }
}
