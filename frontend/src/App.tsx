import StockChart from "./components/StockChart";
import SignUpForm from "./components/SignUpForm";

function App() {
	return (
		<div
			style={{
				padding: "2rem",
				maxWidth: "1200px",
				margin: "0 auto",
				backgroundColor: "#fff",
			}}
		>
			<SignUpForm />
			<StockChart />
		</div>
	);
}

export default App;
