import axios from "axios";

export interface StockData {
	date: string;
	SPY: number;
	SMH: number;
	NVDA: number;
	AMD: number;
}

const calculatePercentageChange = (prices: number[]): number[] => {
	return prices.map((price, index) => {
		if (index === 0) return 0;
		return ((price - prices[0]) / prices[0]) * 100;
	});
};

const calculateRollingAverage = (data: number[], window: number): number[] => {
	return data.map((_, index) => {
		if (index < window - 1) return data[index];
		const slice = data.slice(index - window + 1, index + 1);
		return slice.reduce((sum, value) => sum + value, 0) / window;
	});
};

export const processStockData = async () => {
	const stocks = ["SPY", "SMH", "NVDA", "AMD"];
	const stockData: { [key: string]: number[] } = {};
	const dates: string[] = [];

	for (const stock of stocks) {
		const response = await fetch(`/data/${stock}_historical.csv`);
		const csvText = await response.text();
		const lines = csvText.split("\n").slice(1); // Skip header

		const prices: number[] = [];
		lines.forEach((line) => {
			if (line) {
				const [date, open] = line.split(",");
				if (stock === "SPY") dates.push(date);
				prices.push(parseFloat(open));
			}
		});

		const percentageChanges = calculatePercentageChange(prices);
		stockData[stock] = calculateRollingAverage(percentageChanges, 20);
	}

	return dates.map((date, index) => ({
		date,
		SPY: stockData["SPY"][index],
		SMH: stockData["SMH"][index],
		NVDA: stockData["NVDA"][index],
		AMD: stockData["AMD"][index],
	}));
};
