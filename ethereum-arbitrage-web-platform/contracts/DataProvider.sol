// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";
import "@uniswap/lib/contracts/libraries/Babylonian.sol";
import "libraries/SafeMath.sol";
import "libraries/FullMath.sol";

contract DataProvider {
    using SafeMath for uint256;

    function getEthPrice(address _priceFeed) public view returns (uint256) {
        (, int256 answer, , , ) = AggregatorV3Interface(_priceFeed)
            .latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getTradeData(
        uint256 externalReserveA,
        uint256 externalReserveB,
        uint256 reserveA,
        uint256 reserveB
    ) public pure returns (bool aToB, uint256 amountIn) {
        aToB =
            FullMath.mulDiv(reserveA, externalReserveB, reserveB) <
            externalReserveA;

        uint256 invariant = reserveA.mul(reserveB);

        uint256 leftSide = Babylonian.sqrt(
            FullMath.mulDiv(
                invariant.mul(1000),
                aToB ? externalReserveA : externalReserveB,
                (aToB ? externalReserveB : externalReserveA).mul(997)
            )
        );
        uint256 rightSide = (aToB ? reserveA.mul(1000) : reserveB.mul(1000)) /
            997;

        if (leftSide < rightSide) return (false, 0);

        amountIn = leftSide.sub(rightSide);
    }
}
