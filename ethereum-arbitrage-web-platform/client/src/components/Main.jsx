import { Alert, Snackbar } from "@mui/material";
import Button from "@mui/material/Button";
import { useEthers } from "@usedapp/core";
import { constants, ethers } from "ethers";
import { useEffect, useState } from "react";
import { useCreateOrder, useGetFee, useValidatePair } from "../hooks";
const Input = ({
	placeholder,
	name,
	type,
	value,
	validateInput,
	inputError,
}) => (
	<input
		placeholder={placeholder}
		type={type}
		value={value}
		onChange={(e) => validateInput(e, name)}
		className={`m-4 w-full rounded-sm p-4 outline-dashed outline-2 outline-gray-500 border-none text-md caret-gray-500 placeholder:text-gray-500 placeholder:italic focus:outline-gray-800 focus:outline focus:text-gray-800 ${
			inputError
				? "bg-red-600/20 text-red-700"
				: "bg-slate-400/10 text-gray-500"
		}`}
	/>
);

const Main = () => {
	const { account } = useEthers();

	const [fee, setFee] = useState(0);

	const [input0, setInput0] = useState("");
	const [input1, setInput1] = useState("");

	const [input0Error, setInput0Error] = useState(false);
	const [input1Error, setInput1Error] = useState(false);

	const uniswapPairAddress = useValidatePair("uniswap");
	const sushiswapPairAddress = useValidatePair("sushiswap");

	const getFee = useGetFee();

	useEffect(() => {
		getFee.then((value) => setFee(value));
	}, [getFee]);

	const [pairExists, setPairExists] = useState(false);
	const [showPairAlert, setShowPairAlert] = useState("");

	const [fundSuccessful, setFundSuccessful] = useState(false);
	const [showFundAlert, setShowFundAlert] = useState(false);

	const navbarData = {
		user: account,
		network: "rinkeby",
	};

	const validateInput = (e, name) => {
		setPairExists(false);
		console.log(e.target.value);
		name == "token_0_address"
			? setInput0(e.target.value)
			: setInput1(e.target.value);

		if (
			e.target.value.length != 0 &&
			(e.target.value.length != 42 ||
				!e.target.value.startsWith("0x") ||
				!/^[A-Za-z0-9]*$/.test(e.target.value))
		) {
			name == "token_0_address" ? setInput0Error(true) : setInput1Error(true);
		} else {
			name == "token_0_address" ? setInput0Error(false) : setInput1Error(false);
		}
	};

	const handleSubmit = async () => {
		if (pairExists) {
			let hash;
			await useCreateOrder(input0, input1, fee)
				.then((txHash) => (hash = txHash))
				.catch(() => (hash = "FAILED"));

			if (hash == "FAILED") {
				setFundSuccessful(false);
				setShowFundAlert("FAILED");
			} else {
				setFundSuccessful(true);
				setShowFundAlert(hash);
			}
		} else {
			if (input0 == input1 && input0.length > 0) {
				console.log("Addresses cannot match.");
			} else {
				uniswapPairAddress(input0, input1).then((value) => {
					console.log(value);
					if (value == constants.AddressZero) {
						setPairExists(false);
						setShowPairAlert("Uniswap");
					} else {
						sushiswapPairAddress(input0, input1).then((res) => {
							console.log(res);
							if (res == constants.AddressZero) {
								setPairExists(false);
								setShowPairAlert("Sushiswap");
							} else {
								setPairExists(true);
								setShowPairAlert("true");
							}
						});
					}
				});
			}
		}
	};

	const handleCloseSnack = () => {
		setShowPairAlert("");
		setShowFundAlert("");
	};

	return (
		<>
			<div className="flex w-full justify-center items-center">
				<div className="flex mf:flex-row flex-col items-start justify-between md:p-20 py-12 px-4 w-full">
					<div className="flex flex-col flex-1 items-center justify-start w-full mt-10">
						<div className="p-5 w-2/5 flex flex-col justify-start items-center rounded-lg bg-gradient-to-r from-rose-100/90 to-teal-100/90 drop-shadow-2xl hover:bg-gradient-to-r hover:from-rose-100 hover:to-teal-100">
							<Input
								placeholder="First Token Address"
								name="token_0_address"
								type="text"
								validateInput={validateInput}
								inputError={input0Error}
							/>
							<Input
								placeholder="Second Token Address"
								name="token_1_address"
								type="text"
								validateInput={validateInput}
								inputError={input1Error}
							/>

							<p>Current Fee: {ethers.utils.formatEther(fee.toString())} ETH</p>

							<div className="h-[1px] w-full bg-gray-400 my-2" />

							<Button
								variant="contained"
								onClick={() => handleSubmit()}
								disabled={
									input0Error ||
									input1Error ||
									input0.length == 0 ||
									input1.length == 0 ||
									navbarData["user"] == undefined
								}
								className="mt-3 w-full p-4 rounded-full font-bold  bg-gradient-to-r from-sky-400 to-blue-500 hover:bg-gradient-to-r hover:from-pink-500/80 hover:via-red-500/80 hover:to-yellow-500/80"
							>
								{pairExists ? "Place Order" : "Check Pair Status"}
							</Button>
						</div>
					</div>
				</div>
			</div>

			<Snackbar
				open={showPairAlert.length > 0}
				autoHideDuration={10000}
				onClose={handleCloseSnack}
			>
				<Alert
					onClose={handleCloseSnack}
					severity={pairExists ? "success" : "error"}
				>
					{pairExists
						? "The pair provided is live on both DEXes"
						: `The pair provided does not yet exist on ${showPairAlert}.`}
				</Alert>
			</Snackbar>

			<Snackbar
				open={showFundAlert.length > 0}
				autoHideDuration={10000}
				onClose={handleCloseSnack}
			>
				<Alert
					onClose={handleCloseSnack}
					severity={fundSuccessful ? "success" : "error"}
				>
					{fundSuccessful ? (
						<p>
							Transaction Broadcasted! You can check the transaction out by
							clicking
							<a
								href={`https://rinkeby.etherscan.io/tx/${showFundAlert}`}
								target="_blank"
								rel="noopener noreferrer"
							>
								{" "}
								here
							</a>
						</p>
					) : (
						`Oops. Something went wrong. Please try again in a bit!`
					)}
				</Alert>
			</Snackbar>
		</>
	);
};

export default Main;
