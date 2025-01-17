import StockChart from "./components/StockChart";
import SignUpForm from "./components/SignUpForm";
import Footer from "./components/Footer";

function App() {
	return (
		<div className="flex flex-col min-h-screen relative">
			<main className="flex-1 flex flex-col items-center justify-center py-12 pb-24">
				<div className="w-full max-w-6xl mx-auto px-4">
					<div className="flex flex-col items-center space-y-16">
						<div className="w-full max-w-md">
							<SignUpForm onSubmit={console.log} />
						</div>
						<div className="w-full max-w-2xl">
							<StockChart />
						</div>
					</div>
				</div>
			</main>
			<Footer />
		</div>
	);
}

export default App;
