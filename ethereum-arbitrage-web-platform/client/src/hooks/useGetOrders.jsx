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

const getStatus = (number) => {
	if (number == 0) return "PENDING";
	else if (number == 1) return "COMPLETED";
	else if (number == 2) return "REJECTED";
	else return "DELETED";
};

const useGetOrders = async (address) => {
	let rawOrders = [];
	let orders = [];

	await orderManagerContract
		.getOrders(address)
		.then((res) => {
			rawOrders = res;
			console.log(res, "res");
		})
		.catch((error) => console.log(error));

	rawOrders.forEach((order) => {
		orders.push({
			id: order["id"].toNumber(),
			fee: ethers.utils.formatEther(order["fee"]),
			status: getStatus(order["status"]),
			token0Address: order["token0Address"],
			token1Address: order["token1Address"],
			hash: order["txHash"],
		});
	});

	return orders;
};

export default useGetOrders;
