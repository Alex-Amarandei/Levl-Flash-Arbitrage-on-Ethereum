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
    /// @param _externalReserve0 The price of token 0 on the other exchange
    /// @param _externalReserve1 The price of token 1 on the other exchange
    /// @param _reserve0 The price of token 0 on this exchange
    /// @param _reserve1 The price of token 1 on this exchange
    /**
     * @dev "This" exchange is the exchange from which the flash loan is taken
     * The "other" exchange is the exchange on which the swap is executed
     */
    /// @return The direction of the trade and the maximum amount of tokens to be traded
    function getTradeData(
        uint256 _externalReserve0,
        uint256 _externalReserve1,
        uint256 _reserve0,
        uint256 _reserve1
    ) public pure returns (bool fromAToB, uint256 amountIn) {
        fromAToB =
            FullMath.mulDiv(_reserve0, _externalReserve1, _reserve1) <
            _externalReserve0;

        uint256 leftSide = Babylonian.sqrt(
            FullMath.mulDiv(
                _reserve0.mul(_reserve1).mul(1000),
                fromAToB ? _externalReserve0 : _externalReserve1,
                (fromAToB ? _externalReserve1 : _externalReserve0).mul(997)
            )
        );

        uint256 rightSide = (
            fromAToB ? _reserve0.mul(1000) : _reserve1.mul(1000)
        ) / 997;

        if (leftSide < rightSide) return (false, 0);

        amountIn = leftSide.sub(rightSide);
    }
}
