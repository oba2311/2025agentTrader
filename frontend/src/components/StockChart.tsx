import { useEffect, useState } from "react";
import {
	LineChart,
	Line,
	XAxis,
	YAxis,
	CartesianGrid,
	Tooltip,
	Legend,
	ResponsiveContainer,
} from "recharts";
import { StockData, processStockData } from "../utils/dataProcessor";

const StockChart = () => {
	const [data, setData] = useState<StockData[]>([]);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const processedData = await processStockData();
				setData(processedData);
			} catch (error) {
				console.error("Error fetching stock data:", error);
			}
		};

		fetchData();
	}, []);

	const formatQuarter = (dateStr: string) => {
		const date = new Date(dateStr);
		const quarter = Math.floor(date.getMonth() / 3) + 1;
		return `Q${quarter} ${date.getFullYear()}`;
	};

	const isQuarterStart = (dateStr: string) => {
		const date = new Date(dateStr);
		return date.getMonth() % 3 === 0;
	};

	const renderLabel = (props: any) => {
		const { x, y, value, stroke } = props;
		if (x === undefined || y === undefined) return null;

		// Only show label for the last point
		if (props.index !== data.length - 1) return null;

		return (
			<text
				x={x}
				y={y}
				dx={10}
				dy={3}
				fill={stroke}
				fontSize={12}
				textAnchor="start"
			>
				{props.name}
			</text>
		);
	};

	return (
		<div style={{ width: "100%", height: "80vh" }}>
			<h1 style={{ textAlign: "center", marginBottom: "2rem" }}>
				20-Day Rolling Average Performance (% Change)
			</h1>
			<ResponsiveContainer>
				<LineChart data={data} margin={{ right: 80 }}>
					<CartesianGrid strokeDasharray="3 3" />
					<XAxis
						dataKey="date"
						tickFormatter={formatQuarter}
						ticks={data
							.filter((d) => isQuarterStart(d.date))
							.map((d) => d.date)}
					/>
					<YAxis
						label={{
							value: "Percentage Change (%)",
							angle: -90,
							position: "insideLeft",
						}}
					/>
					<Tooltip
						labelFormatter={(date) => new Date(date).toLocaleDateString()}
						formatter={(value: number) => [value.toFixed(2) + "%"]}
					/>
					<Legend />
					<Line
						type="monotone"
						dataKey="SPY"
						stroke="#8884d8"
						name="S&P 500 (SPY)"
						dot={false}
						strokeWidth={3}
						label={renderLabel}
					/>
					<Line
						type="monotone"
						dataKey="SMH"
						stroke="#82ca9d"
						name="Semiconductor ETF (SMH)"
						dot={false}
						label={renderLabel}
					/>
					<Line
						type="monotone"
						dataKey="NVDA"
						stroke="#ff7300"
						name="NVIDIA"
						dot={false}
						label={renderLabel}
					/>
					<Line
						type="monotone"
						dataKey="AMD"
						stroke="#ff0000"
						name="AMD"
						dot={false}
						label={renderLabel}
					/>
				</LineChart>
			</ResponsiveContainer>
		</div>
	);
};

export default StockChart;
