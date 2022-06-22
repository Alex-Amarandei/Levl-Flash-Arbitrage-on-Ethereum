import ReceiptIcon from "@mui/icons-material/Receipt";
import {
	Alert,
	Button,
	Card,
	CardContent,
	Chip,
	Divider,
	Drawer,
	Snackbar,
	Typography,
} from "@mui/material";
import { Fragment, useEffect, useState } from "react";
import { useGetOrders, useRefundGas } from "../hooks";

const Menus = () => {
	const getOrders = useGetOrders(ethereum.selectedAddress);

	const [orders, setOrders] = useState([]);

	const [menuShowing, setMenuShowing] = useState({
		left: false,
		right: false,
	});

	const [refundSuccessful, setRefundSuccessful] = useState(false);
	const [showRefundAlert, setShowRefundAlert] = useState(false);

	const handleCloseSnack = () => {
		setShowRefundAlert("");
	};

	const cancelOrderHandler = async (id, all) => {
		let hash;
		await useRefundGas(id, all)
			.then((txHash) => (hash = txHash))
			.catch(() => (hash = "FAILED"));

		if (hash == "FAILED") {
			setRefundSuccessful(false);
			setShowRefundAlert("FAILED");
		} else {
			setRefundSuccessful(true);
			setShowRefundAlert(hash);
			cancelOrder(id, all);
		}
	};

	const card = (element) => (
		<Fragment>
			<CardContent>
				<div
					style={{
						display: "flex",
						justifyContent: "space-between",
						marginBottom: 10,
						alignItems: "center",
					}}
				>
					<Chip
						sx={{
							marginLeft: 1,
						}}
						component={"span"}
						label={"#" + element["id"]}
						variant="filled"
					/>
					<Typography
						component={"span"}
						variant="body2"
						color={
							element["status"] == "PENDING"
								? "#EAB308"
								: element["status"] == "COMPLETED"
								? "#16A34A"
								: "#C60D25"
						}
						gutterBottom
						sx={{ display: "block" }}
					>
						{element["status"]}
					</Typography>
					{element["status"] == "PENDING" || element["status"] == "REJECTED" ? (
						<Chip
							sx={{
								marginRight: 1,
							}}
							component={"span"}
							label={"X"}
							variant="filled"
							color="warning"
							clickable
							onClick={() => cancelOrderHandler(element["id"], false)}
						/>
					) : (
						<></>
					)}
				</div>

				<Divider>
					<Typography component={"span"} color="gray" sx={{ display: "block" }}>
						Details
					</Typography>
				</Divider>
				<Typography
					component={"span"}
					variant="subtitle1"
					style={{
						padding: 10,
						margin: 5,
					}}
					sx={{ display: "block" }}
				>
					First Token:{" "}
					<Chip
						label={
							element["token0Address"].slice(0, 6) +
							"..." +
							element["token0Address"].slice(36)
						}
						component="a"
						href={`https://rinkeby.etherscan.io/address/${element["token0Address"]}`}
						target="_blank"
						rel="noopener noreferrer"
						variant="filled"
						color="info"
						clickable
					/>
				</Typography>
				<Typography
					component={"span"}
					variant="subtitle1"
					style={{
						padding: 10,
						margin: 5,
					}}
					sx={{ display: "block" }}
				>
					Second Token:{" "}
					<Chip
						label={
							element["token1Address"].slice(0, 6) +
							"..." +
							element["token1Address"].slice(36)
						}
						component="a"
						href={`https://rinkeby.etherscan.io/address/${element["token1Address"]}`}
						variant="filled"
						target="_blank"
						rel="noopener noreferrer"
						color="info"
						clickable
					/>
				</Typography>
				<Typography
					component={"span"}
					align="center"
					variant="overline"
					sx={{ display: "block" }}
				>
					Fee: {element["fee"]} ETH
				</Typography>
			</CardContent>
			{element["status"] == "COMPLETED" ? (
				<div align="center" className="chipReceipt">
					<Chip
						component="a"
						href={`https://rinkeby.etherscan.io/tx/${element["hash"]}`}
						variant="filled"
						target="_blank"
						rel="noopener noreferrer"
						label="Transaction Receipt"
						color="secondary"
						icon={<ReceiptIcon />}
						clickable
					/>
				</div>
			) : (
				<></>
			)}
		</Fragment>
	);

	useEffect(() => {
		getOrders.then((res) => {
			res.reverse();
			setOrders(res);
		});
	}, []);

	const toggleDrawer = (anchor, open) => (event) => {
		if (
			event.type === "keydown" &&
			(event.key === "Tab" || event.key === "Shift")
		) {
			return;
		}

		setMenuShowing({ ...menuShowing, [anchor]: open });
	};

	return (
		<>
			<div className="w-1/3">
				<ul className="text-white md:flex hidden list-none flex-row justify-start items-center flex-initial capitalize">
					<Button
						variant="contained"
						className="rounded-full bg-slate-50/50 shadow-lg px-6 py-3 font-bold mx-4"
						onClick={toggleDrawer("left", true)}
					>
						Orders
					</Button>
					<Drawer
						anchor={"left"}
						open={menuShowing["left"]}
						onClose={toggleDrawer("left", false)}
					>
						{orders.map((element) => (
							<>
								<Card
									variant="outlined"
									style={{
										backgroundColor: "#dbe9f4",
										minHeight: 300,
									}}
								>
									{card(element)}
								</Card>
								<Divider sx={{ background: "#8b5cf6" }} />
							</>
						))}
					</Drawer>
					<Button
						variant="contained"
						className="rounded-full bg-slate-50/50 shadow-lg px-6 py-3 font-bold mx-4"
						onClick={toggleDrawer("right", true)}
					>
						Info
					</Button>
					<Drawer
						anchor={"right"}
						open={menuShowing["right"]}
						onClose={toggleDrawer("right", false)}
					>
						<>
							<Card
								variant="outlined"
								style={{
									backgroundColor: "#dbe9f4",
									minHeight: 200,
								}}
							>
								<Fragment>
									<CardContent sx={{ width: "50vw", height: "100vh" }}>
										<Typography variant="h2" align="center" gutterBottom>
											Welcome to Levl!
										</Typography>
										<Divider gutterBottom>
											<Typography
												variant="subititle1"
												align="center"
												gutterBottom
											>
												⚡️ Arbitrage using Flash Swaps ⚡️
											</Typography>
										</Divider>
										<br />
										<Typography variant="h6" align="center">
											👍 Here are a few tips to help you get started 👍
										</Typography>
										<br />
										<Divider>
											<Typography variant="h5" gutterBottom>
												🔗 <b>Connecting Your Wallet</b>
											</Typography>
										</Divider>

										<Typography
											variant="body1"
											style={{ textIndent: 50 }}
											gutterBottom
										>
											Just hit the <i>Connect Wallet</i> button and accept the
											request for connecting in your MetaMask. You will be shown
											your current address and the chain on which you are now.
											We currently only support the Rinkeby network.
										</Typography>
										<br />
										<Divider>
											<Typography variant="h5" gutterBottom>
												🪙 <b>Choosing Tokens</b>
											</Typography>
										</Divider>
										<Typography
											variant="body1"
											style={{ textIndent: 50 }}
											gutterBottom
										>
											<i>Arbitrage</i> is based on taking advantage of
											differences in pricing across different markets, so it
											makes sense that newer, more volatile pairs have a slight
											edge over well-established pairs <i>(such as DAI/WETH)</i>{" "}
											or stable pairs <i>(such as DAI/USDC)</i>.
											<br />
											Although, you never know 🤷‍♂️
										</Typography>

										<Divider>
											<Typography variant="h5" gutterBottom>
												⚙️ <b>Using Levl</b>
											</Typography>
										</Divider>

										<Typography
											variant="body1"
											style={{ textIndent: 50 }}
											gutterBottom
										>
											1️⃣ Provide the address of the tokens you chose 📭
										</Typography>
										<Typography
											variant="body1"
											style={{ textIndent: 50 }}
											gutterBottom
										>
											2️⃣ We will check if there is liquidity for the pair on
											both Uniswap and Sushiswap ✅
										</Typography>
										<Typography
											variant="body1"
											style={{ textIndent: 50 }}
											gutterBottom
										>
											3️⃣ Sign the transaction for paying the compensation fee
											(for the gas used) 💰
										</Typography>
										<Typography
											variant="body1"
											style={{ textIndent: 50 }}
											gutterBottom
										>
											4️⃣ Sit back and relax while we take care of fulfilling
											your order. Your profits will be sent to you and your
											order's status will be updated 💸
										</Typography>
										<Typography
											variant="body1"
											style={{ textIndent: 50 }}
											gutterBottom
										>
											5️⃣ In the unfortunate event that your order is rejected
											due to technical reasons or that you decide to cancel it,
											no worries, your fee will be refunded 👌🏻
										</Typography>

										<Divider>
											<Typography variant="h5" gutterBottom>
												🤩 <b>Happy Capital-Free Arbitraging!</b> 🥳
											</Typography>
										</Divider>
									</CardContent>
								</Fragment>
							</Card>
						</>
					</Drawer>
				</ul>
			</div>
			<Snackbar
				open={showRefundAlert.length > 0}
				autoHideDuration={10000}
				onClose={handleCloseSnack}
			>
				<Alert
					onClose={handleCloseSnack}
					severity={refundSuccessful ? "success" : "error"}
				>
					{refundSuccessful ? (
						<p>
							Transaction Broadcasted! You can check the transaction out by
							clicking
							<a
								href={`https://rinkeby.etherscan.io/tx/${showRefundAlert}`}
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

export default Menus;
