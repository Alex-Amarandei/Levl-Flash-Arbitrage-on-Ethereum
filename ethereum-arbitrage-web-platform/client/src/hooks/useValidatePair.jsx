import { ethers } from "ethers";
import brownieJson from "../brownieConfig.json";
import factoryJson from "../contract_builds/interfaces/IUniswapV2Factory.json";

const provider = new ethers.providers.Web3Provider(ethereum);

const factoryAbi = factoryJson["abi"];

const useValidatePair = (dex) => {
	const factoryAddress = brownieJson["networks"]["rinkeby"]["factory"][dex];
	const factoryContract = new ethers.Contract(
		factoryAddress,
		factoryAbi,
		provider
	);

	const pairAddress = async (token0Address, token1Address) => {
		return await factoryContract.getPair(token0Address, token1Address);
	};

	return pairAddress;
};

export default useValidatePair;
