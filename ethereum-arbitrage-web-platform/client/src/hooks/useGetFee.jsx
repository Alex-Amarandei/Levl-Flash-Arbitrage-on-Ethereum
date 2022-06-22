import { ethers } from "ethers";
import orderManagerJson from "../contract_builds/contracts/OrderManager.json";
import mapJson from "../contract_builds/deployments/map.json";

const provider = new ethers.providers.Web3Provider(ethereum);
const orderManagerAbi = orderManagerJson["abi"];
const orderManagerAddress = mapJson["4"]["OrderManager"][0];
const orderManagerContract = new ethers.Contract(
	orderManagerAddress,
	orderManagerAbi,
	provider
);

const useGetFee = async () => {
	const getFee = await orderManagerContract.fee();
	return getFee;
};

export default useGetFee;
