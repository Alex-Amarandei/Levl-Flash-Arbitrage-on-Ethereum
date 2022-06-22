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

const useRefundGas = async (id, all) => {
	let txHash;

	await orderManagerContract
		.refundGas(id, all)
		.then((tx) => {
			console.log(tx);
			txHash = tx["hash"];
		})
		.catch((error) => {
			console.error(error);
			txHash = "FAILED";
		});

	return txHash;
};

export default useRefundGas;
