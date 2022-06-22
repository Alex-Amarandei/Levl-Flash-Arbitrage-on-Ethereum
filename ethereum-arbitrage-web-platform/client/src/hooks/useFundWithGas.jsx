import { ethers } from "ethers";
import fundsManagerJson from "../contract_builds/contracts/FundsManager.json";
import mapJson from "../contract_builds/deployments/map.json";

const provider = new ethers.providers.Web3Provider(ethereum);

const fundsManagerAddress = mapJson["4"]["FundsManager"][0];
const fundsManagerAbi = fundsManagerJson["abi"];
const fundsManagerContract = new ethers.Contract(
	fundsManagerAddress,
	fundsManagerAbi,
	provider.getSigner()
);

const useFundWithGas = async (feeInWei) => {
	let txHash;
	await fundsManagerContract
		.fundWithGas({
			value: feeInWei.toHexString(),
		})
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

export default useFundWithGas;
