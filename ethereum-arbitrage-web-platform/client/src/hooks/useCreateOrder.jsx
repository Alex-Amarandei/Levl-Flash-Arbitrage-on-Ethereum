import { ethers } from "ethers";
import orderManagerJson from "../contract_builds/contracts/OrderManager.json";
import mapJson from "../contract_builds/deployments/map.json";

const provider = new ethers.providers.Web3Provider(ethereum);

const orderManagerAddress = mapJson["4"]["OrderManager"][0];
const orderManagerAbi = orderManagerJson["abi"];
const orderManagerContract = new ethers.Contract(
	orderManagerAddress,
	orderManagerAbi,
	provider.getSigner()
);

const useCreateOrder = async (token0Address, token1Address, feeInWei) => {
	let txHash;

	await orderManagerContract
		.createOrder(token0Address, token1Address, {
			value: feeInWei.toHexString(),
		})
		.then((tx) => {
			txHash = tx["hash"];
			console.log(tx);
		})
		.catch((error) => {
			txHash = "FAILED";
			console.error(error);
		});

	return txHash;
};

export default useCreateOrder;
